@nightyScript(
    name="JSON Storage Example",
    author="thedorekaczynski",
    description="Demonstrates the use of JSON storage for persistent data",
    usage="<p>json add <item> OR <p>json remove <item> OR <p>json list"
)
def json_storage_example():
    """
    JSON Storage Example
    ------------------
    
    This script demonstrates how to use JSON storage for persistent data.
    It maintains a list of items that persists between script restarts.
    
    COMMANDS:
    <p>json add <item> - Add an item to the list
    <p>json remove <item> - Remove an item from the list
    <p>json list - List all items
    
    EXAMPLES:
    <p>json add apple - Add 'apple' to the list
    <p>json remove apple - Remove 'apple' from the list
    <p>json list - Show all items in the list
    
    NOTES:
    - Data is stored in a JSON file in the json/ directory
    - The file is created automatically if it doesn't exist
    """
    
    import json
    from pathlib import Path
    
    # Define the JSON file path
    BASE_DIR = Path(getScriptsPath()) / "json"
    DATA_FILE = BASE_DIR / "json_example_data.json"
    
    # Ensure the directory exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize the file if it doesn't exist
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w") as f:
            json.dump({"items": []}, f, indent=4)
    
    # Helper functions for loading and saving data
    def load_data():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"items": []}
    
    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    
    @bot.command(name="json", description="Manage items in JSON storage")
    async def json_command(ctx, *, args: str):
        await ctx.message.delete()
        
        # Split the arguments
        parts = args.strip().split(maxsplit=1)
        if not parts:
            await ctx.send("Usage: `<p>json add <item>` OR `<p>json remove <item>` OR `<p>json list`")
            return
            
        action = parts[0].lower()
        
        if action == "list":
            # Load and display all items
            data = load_data()
            items = data.get("items", [])
            
            if not items:
                await ctx.send("No items in the list.")
            else:
                await ctx.send(f"Items: {', '.join(items)}")
                
        elif action in ["add", "remove"]:
            if len(parts) < 2:
                await ctx.send(f"Usage: `<p>json {action} <item>`")
                return
                
            item = parts[1]
            data = load_data()
            items = data.get("items", [])
            
            if action == "add":
                if item in items:
                    await ctx.send(f"Item '{item}' is already in the list.")
                else:
                    items.append(item)
                    data["items"] = items
                    save_data(data)
                    await ctx.send(f"Added '{item}' to the list.")
                    
            elif action == "remove":
                if item not in items:
                    await ctx.send(f"Item '{item}' is not in the list.")
                else:
                    items.remove(item)
                    data["items"] = items
                    save_data(data)
                    await ctx.send(f"Removed '{item}' from the list.")
                    
        else:
            await ctx.send("Invalid action. Use 'add', 'remove', or 'list'.")

json_storage_example()  # Call to initialize 