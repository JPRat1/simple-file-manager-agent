
# AI File Manager Agent

An AI-powered file management assistant built with Python, Pydantic AI, OpenAI, and the Model Context Protocol (MCP).

## Features

- AI-powered file management
- Filesystem access through MCP
- Conversation memory
- Persistent conversation history
- OpenAI API integration
- Configurable workspace directory

## Requirements

- Python
- Node.js and npm
- OpenAI API key

## Installation

Install the Python dependencies:

    pip install -r requirements.txt

## Configuration

Set your OpenAI API key as a Windows environment variable:

    setx OPENAI_API_KEY "your-api-key"

Restart your terminal after setting the variable.

## Running the Agent

    python agent.py

## Technologies

- Python
- Pydantic AI
- OpenAI API
- Model Context Protocol
- FastMCP
