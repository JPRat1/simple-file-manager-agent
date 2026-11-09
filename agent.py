from pathlib import Path
from pydantic_ai import ModelMessagesTypeAdapter
from pydantic_core import to_json
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from fastmcp.client.transports import StdioTransport
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

WORKSPACE = Path(r"C:\Users\Strai\Downloads")

HISTORY_FILE = (
    Path.home() / "Downloads"
)
# Connect to the existing filesystem MCP server
filesystem = MCPToolset(
    StdioTransport(
        command="cmd",
        args=[
            "/c",
            "npx",
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(WORKSPACE),
        ],
    )
)

# Configure your AI model
model = OpenAIChatModel(
    model_name="gpt-5.5",
    provider=OpenAIProvider(),
)

# Create your agent
agent = Agent(
    model=model,
    toolsets=[filesystem],
    system_prompt=(
        "You are a privacy-focused file management assistant. "
        "Use the available filesystem tools to manage files. "
        "Never invent file contents or claim an operation succeeded "
        "unless the tool confirms it. "
        "Ask for confirmation before deleting or modifying files. And if a file contains personal information (or PII) never read it or redact  it"
    ),
)

if __name__ == "__main__":
    print("File Manager Agent Initialized!")

    if HISTORY_FILE.exists():
        message_history = ModelMessagesTypeAdapter.validate_json(
            HISTORY_FILE.read_bytes()
        )
        print("Previous conversation restored!")
    else:
        message_history = []
        print("Starting a new conversation")    

    while True:
        try:
            instruction = input("\nYou: ")

            if instruction.lower().strip() in ["exit", "quit"]:
                break

            if not instruction.strip():
                continue
            
            if instruction.strip().lower() == "/new":
                message_history = []
                HISTORY_FILE.unlink(missing_ok=True)
                print("Conversation cleared!")
                continue

            print("\nAgent is thinking...")

            result = agent.run_sync(
                instruction,
                message_history=message_history,
            )

            # IMPORTANT: Update conversation history
            message_history = result.all_messages()

            # IMPORTANT: Save conversation to disk
            HISTORY_FILE.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            HISTORY_FILE.write_bytes(
                to_json(message_history)
            )

            print("\nAgent:", result.output)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

            