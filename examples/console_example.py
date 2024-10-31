"""Example of enhanced console capabilities."""
from pepperpy.console import (
    PeppyConsole,
    ConsoleConfig,
    print_message,
    print_table,
    print_code,
    print_markdown,
    get_input,
    get_confirmation
)

def demonstrate_console():
    # Custom console with configuration
    config = ConsoleConfig(
        theme={
            "info": "cyan",
            "success": "green bold",
            "warning": "yellow",
            "error": "red bold",
            "title": "blue bold"
        },
        emoji=True
    )
    console = PeppyConsole(config)
    
    # Title and messages
    console.title("🚀 Pepperpy Console Demo")
    console.info("Starting demonstration...")
    console.success("Operation completed!")
    console.warning("Resource usage high")
    console.error("Connection failed")
    
    # Tables
    data = [
        {"Name": "Alice", "Role": "Developer", "Team": "Backend"},
        {"Name": "Bob", "Role": "Designer", "Team": "UI/UX"},
        {"Name": "Charlie", "Role": "Manager", "Team": "Product"}
    ]
    console.title("📊 Team Members")
    console.table(data)
    
    # Code highlighting
    code = '''
def hello_world():
    """Say hello to the world."""
    print("Hello, World!")
    return True
    '''
    console.title("💻 Sample Code")
    console.code(code, language="python")
    
    # Markdown
    markdown = """
    # Project Overview
    
    ## Features
    - Easy to use
    - Highly configurable
    - Beautiful output
    
    ## Installation
    ```bash
    pip install pepperpy
    ```
    """
    console.title("📝 Documentation")
    console.markdown(markdown)
    
    # Tree structure
    data = {
        "project": {
            "src": {
                "main.py": "Main module",
                "utils.py": "Utilities"
            },
            "tests": {
                "test_main.py": "Main tests",
                "test_utils.py": "Utility tests"
            },
            "docs": {
                "index.md": "Documentation"
            }
        }
    }
    console.title("🌳 Project Structure")
    console.tree(data)
    
    # Progress tracking
    console.title("⏳ Processing")
    with console.progress("Processing items") as update:
        for i in range(100):
            # Simulate work
            update()
    
    # User input
    name = console.prompt("What's your name?", default="User")
    console.info(f"Hello, {name}!")
    
    if console.confirm("Would you like to continue?"):
        console.success("Continuing...")
    else:
        console.warning("Stopping...")

if __name__ == "__main__":
    demonstrate_console() 