# Calculator MCP Server v2.0

A modular calculator MCP server for Claude Code that provides comprehensive math operations and interactive prompts.

## Features

- **9 Math & Statistical Operations**: Addition, subtraction, multiplication, division, square, square root, nth root, cube, average
- **Interactive Prompts**: Multiplication table prompt with customizable size and starting numbers
- **Statistical Functions**: Calculate arithmetic mean of number lists with comprehensive validation
- **Modular Architecture**: Each operation and prompt is implemented as a separate module (<200 lines)
- **Claude Code Integration**: Project-level `.mcp.json` configuration for seamless integration
- **Type Safety**: Full Pydantic model validation for inputs and outputs
- **Bilingual Support**: Chinese and English output support for prompts
- **Error Handling**: Comprehensive error handling with Chinese language support

## Installation

1. Clone this repository
2. Install dependencies: `uv sync`
3. The `.mcp.json` file will be automatically detected by Claude Code

## Usage

Once configured in Claude Code, you can use the calculator by asking Claude to perform math operations and use interactive prompts:

### Math Operations
```
Calculate the square root of 25
Calculate 10 + 5 * 3
Use calculator to compute the 10th root of 2
```

### Statistical Operations
```
Calculate the average of these numbers: [1, 2, 3, 4, 5]
Find the mean value: [10.5, 20.3, 15.7, 18.9]
Compute average: [-5, 0, 5, 10, 15]
```

### Interactive Prompts (New in v2.0)
```
Create a 5x5 multiplication table starting from 1
Generate a multiplication table with size 3 starting from 5 in English
Generate a 4x4 multiplication table starting from -2 in table format
Create a multiplication table with size 6 starting from 0 in list format
```

## Project Structure

```
src/calculator_mcp/
├── base/          # Base framework classes and registries
├── operations/    # Individual math operation modules  
├── prompts/       # Interactive prompt modules (New in v2.0)
├── utils/         # Utility functions
└── server.py      # Main server entry point
```

## Development

- Run tests: `uv run pytest`
- Start server: `uv run python src/calculator_mcp/server.py`