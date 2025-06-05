@nightyScript(
    name="Selective Event Example",
    author="thedorekaczynski",
    description="Demonstrates selective event handling with JSON storage",
    usage="<p>selective addserver <server_id> OR <p>selective adduser <user_id> OR <p>selective list"
)
def selective_event_example():
    """
    Selective Event Example
    ---------------------
    
    This script demonstrates how to use selective event handling with JSON storage.
    It only responds to messages from specific servers and users.
    
    COMMANDS:
    <p>selective addserver <server_id> - Add a server to the allowed list
    <p>selective adduser <user_id> - Add a user to the allowed list
    <p>selective list - List all allowed servers and users
    
    EXAMPLES:
    <p>selective addserver 123456789 - Add server with ID 123456789 to the allowed list
    <p>selective adduser 987654321 - Add user with ID 987654321 to the allowed list
    <p>selective list - Show all allowed servers and users
    
    NOTES:
    - The script ONLY responds to messages from servers and users in the allowed lists
    - If no servers or users are in the allowed list, the event listener will not respond to any messages
    - The allowed lists are stored in JSON files in the json/ directory
    """
    
    import json
    from pathlib import Path
    
    # Define the JSON file paths
    BASE_DIR = Path(getScriptsPath()) / "json"
    SERVERS_FILE = BASE_DIR / "selective_servers.json"
    USERS_FILE = BASE_DIR / "selective_users.json"
    
    # Ensure the directory exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize the files if they don't exist
    if not SERVERS_FILE.exists():
        with open(SERVERS_FILE, "w") as f:
            json.dump([], f, indent=4)
            
    if not USERS_FILE.exists():
        with open(USERS_FILE, "w") as f:
            json.dump([], f, indent=4)
    
    # Helper functions for loading and saving data
    def load_ids(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_ids(file_path, id_list):
        with open(file_path, "w") as f:
            json.dump(id_list, f, indent=4)
    
    @bot.command(name="selective", description="Manage allowed servers and users")
    async def selective_command(ctx, *, args: str):
        await ctx.message.delete()
        
        # Split the arguments
        parts = args.strip().split(maxsplit=2)
        if len(parts) < 2:
            await ctx.send("Usage: `<p>selective addserver <server_id>` OR `<p>selective adduser <user_id>` OR `<p>selective list`")
            return
            
        action = parts[0].lower()
        
        if action == "list":
            # Load and display all allowed servers and users
            allowed_servers = load_ids(SERVERS_FILE)
            allowed_users = load_ids(USERS_FILE)
            
            server_text = "Allowed Servers: " + ", ".join(allowed_servers) if allowed_servers else "None"
            user_text = "Allowed Users: " + ", ".join(allowed_users) if allowed_users else "None"
            
            await ctx.send(f"{server_text}\n{user_text}")
            
        elif action == "addserver":
            server_id = parts[1]
            try:
                # Validate as integer
                server_id = str(int(server_id))
                
                # Check if the server exists
                server = bot.get_guild(int(server_id))
                if not server:
                    await ctx.send(f"Server with ID {server_id} not found.")
                    return
                    
                # Add the server to the allowed list
                allowed_servers = load_ids(SERVERS_FILE)
                if server_id not in allowed_servers:
                    allowed_servers.append(server_id)
                    save_ids(SERVERS_FILE, allowed_servers)
                    await ctx.send(f"Added server {server.name} ({server_id}) to the allowed list.")
                else:
                    await ctx.send(f"Server {server.name} ({server_id}) is already in the allowed list.")
                    
            except ValueError:
                await ctx.send("Invalid server ID. Please provide a valid ID.")
                
        elif action == "adduser":
            user_id = parts[1]
            try:
                # Validate as integer
                user_id = str(int(user_id))
                
                # Add the user to the allowed list
                allowed_users = load_ids(USERS_FILE)
                if user_id not in allowed_users:
                    allowed_users.append(user_id)
                    save_ids(USERS_FILE, allowed_users)
                    await ctx.send(f"Added user {user_id} to the allowed list.")
                else:
                    await ctx.send(f"User {user_id} is already in the allowed list.")
                    
            except ValueError:
                await ctx.send("Invalid user ID. Please provide a valid ID.")
                
        else:
            await ctx.send("Invalid action. Use 'addserver', 'adduser', or 'list'.")
    
    @bot.listen("on_message")
    async def message_handler(message):
        # Ignore messages from the bot itself
        if message.author.id == bot.user.id:
            return
            
        # Load allowed servers and users
        allowed_servers = load_ids(SERVERS_FILE)
        allowed_users = load_ids(USERS_FILE)
        
        # Check if the message is from an allowed server or user
        server_id = str(message.guild.id) if message.guild else None
        user_id = str(message.author.id)
        
        # Only respond if the message is from an allowed server AND an allowed user
        # If either list is empty, we don't respond to any messages
        if not allowed_servers or not allowed_users:
            return
            
        # Check if the message is from an allowed server
        if server_id and server_id not in allowed_servers:
            return
            
        # Check if the message is from an allowed user
        if user_id not in allowed_users:
            return
            
        # Respond to the message
        await message.channel.send(f"Hello, {message.author.mention}! I noticed your message: {message.content}")

selective_event_example()  # Call to initialize 