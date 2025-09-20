# Calculator MCP Server

A modular calculator MCP server for Claude Code that provides comprehensive math operations.

## Features

- **8 Math Operations**: Addition, subtraction, multiplication, division, square, square root, nth root, cube
- **Modular Architecture**: Each operation is implemented as a separate module (<200 lines)
- **Claude Code Integration**: Project-level `.mcp.json` configuration for seamless integration
- **Type Safety**: Full Pydantic model validation for inputs and outputs
- **Error Handling**: Comprehensive error handling with Chinese language support

## Installation

1. Clone this repository
2. Install dependencies: `uv sync`
3. The `.mcp.json` file will be automatically detected by Claude Code

## Usage

Once configured in Claude Code, you can use the calculator by asking Claude to perform math operations:

```
Calculate the square root of 25
Calculate 10 + 5 * 3
Use calculator to compute the 10th root of 2
```

## Project Structure

```
src/calculator_mcp/
├── base/          # Base framework classes
├── operations/    # Individual math operation modules  
├── utils/         # Utility functions
└── server.py      # Main server entry point
```

## Development

- Run tests: `uv run pytest`
- Start server: `uv run python src/calculator_mcp/server.py`