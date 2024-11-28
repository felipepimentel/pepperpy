# PepperPy Console Examples

This directory contains examples demonstrating the capabilities of the pepperpy-console package.

## Examples

### Chat Interface (chat_interface.py)
Demonstrates how to build an interactive chat interface with:
- Chat message display
- Input field
- Send button
- Streaming AI responses
- Layout management

```bash
python chat_interface.py
```

### Progress Tracker (progress_tracker.py)
Shows how to create a progress tracking interface with:
- Progress bar
- Task details table
- Real-time updates
- Layout management

```bash
python progress_tracker.py
```

## Running Examples

1. Make sure you have pepperpy-console installed:
```bash
poetry install
```

2. Navigate to the examples directory:
```bash
cd examples
```

3. Run any example:
```bash
poetry run python chat_interface.py
```

## Creating Your Own Examples

Feel free to use these examples as templates for your own console applications. Key components you can use:

- `Console`: Main console interface
- `Layout`: Organize UI elements
- `Panel`: Frame content
- `ChatView`: Display chat messages
- `Input`: Text input field
- `Button`: Interactive button
- `ProgressBar`: Show progress
- `Table`: Display tabular data
- And more!

Check the main package documentation for detailed API information.
