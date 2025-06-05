@nightyScript(
    name="Subcommand Example",
    author="thedorekaczynski",
    description="Demonstrates the use of bot commands with subcommands",
    usage="<p>todo <subcommand> [args]"
)
def subcommand_example():
    """
    Subcommand Example
    ----------------
    
    This script demonstrates how to use bot commands with subcommands.
    It implements a simple todo list manager with subcommands.
    
    COMMANDS:
    <p>todo add <item> - Add an item to the todo list
    <p>todo remove <index> - Remove an item from the todo list
    <p>todo list - List all items in the todo list
    <p>todo help - Show help information
    
    EXAMPLES:
    <p>todo add Buy groceries - Add 'Buy groceries' to the todo list
    <p>todo remove 1 - Remove the first item from the todo list
    <p>todo list - Show all items in the todo list
    <p>todo help - Show help information
    
    NOTES:
    - The todo list is stored in memory and will be reset when the script is reloaded
    - For persistent storage, use the JSON storage example
    """
    
    # Store the todo list in memory
    todo_list = []
    
    @bot.command(name="todo", description="Manage a todo list with subcommands")
    async def todo_command(ctx, *, args: str):
        await ctx.message.delete()
        
        # Split args into subcommand and arguments
        parts = args.strip().split(maxsplit=1)
        subcommand = parts[0].lower() if parts else ""
        subargs = parts[1] if len(parts) > 1 else ""
        
        # Handle subcommands
        if subcommand == "add":
            if not subargs:
                await ctx.send("Usage: `<p>todo add <item>`")
                return
                
            todo_list.append(subargs)
            await ctx.send(f"Added: {subargs}")
            
        elif subcommand == "remove":
            if not subargs:
                await ctx.send("Usage: `<p>todo remove <index>`")
                return
                
            try:
                index = int(subargs) - 1  # Convert to 0-based index
                if index < 0 or index >= len(todo_list):
                    await ctx.send(f"Invalid index. Use a number between 1 and {len(todo_list)}.")
                    return
                    
                removed_item = todo_list.pop(index)
                await ctx.send(f"Removed: {removed_item}")
                
            except ValueError:
                await ctx.send("Invalid index. Please provide a number.")
                
        elif subcommand == "list":
            if not todo_list:
                await ctx.send("Todo list is empty.")
                return
                
            # Create a numbered list
            todo_text = "**Todo List:**\n"
            for i, item in enumerate(todo_list, 1):
                todo_text += f"{i}. {item}\n"
                
            await ctx.send(todo_text)
            
        elif subcommand == "help":
            help_text = """
**Todo List Help**

**Commands:**
`<p>todo add <item>` - Add an item to the todo list
`<p>todo remove <index>` - Remove an item from the todo list
`<p>todo list` - List all items in the todo list
`<p>todo help` - Show this help message

**Examples:**
`<p>todo add Buy groceries` - Add 'Buy groceries' to the todo list
`<p>todo remove 1` - Remove the first item from the todo list
`<p>todo list` - Show all items in the todo list
"""
            await ctx.send(help_text)
            
        else:
            await ctx.send("Invalid subcommand. Use 'add', 'remove', 'list', or 'help'.")

subcommand_example()  # Call to initialize 