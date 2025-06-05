@nightyScript(
    name="Config Example",
    author="thedorekaczynski",
    description="Demonstrates the use of getConfigData and updateConfigData functions",
    usage="<p>config get <key> OR <p>config set <key> <value>"
)
def config_example():
    """
    Config Example
    -------------
    
    This script demonstrates how to use the getConfigData and updateConfigData functions
    to store and retrieve configuration values.
    
    COMMANDS:
    <p>config get <key> - Get the value of a configuration key
    <p>config set <key> <value> - Set the value of a configuration key
    
    EXAMPLES:
    <p>config get my_setting - Get the value of 'my_setting'
    <p>config set my_setting true - Set 'my_setting' to 'true'
    
    NOTES:
    - Configuration values persist between script restarts
    - Use .get(key, default) to provide a default value if the key is not set
    """
    
    @bot.command(name="config", description="Get or set configuration values")
    async def config_command(ctx, *, args: str):
        await ctx.message.delete()
        
        # Split the arguments
        parts = args.strip().split(maxsplit=2)
        if len(parts) < 2:
            await ctx.send("Usage: `<p>config get <key>` OR `<p>config set <key> <value>`")
            return
            
        action = parts[0].lower()
        key = parts[1]
        
        if action == "get":
            # Get the configuration value
            value = getConfigData().get(key, "Not set")
            await ctx.send(f"Config value for '{key}': {value}")
            
        elif action == "set":
            if len(parts) < 3:
                await ctx.send("Usage: `<p>config set <key> <value>`")
                return
                
            value = parts[2]
            # Update the configuration value
            updateConfigData(key, value)
            await ctx.send(f"Set '{key}' to '{value}'")
            
        else:
            await ctx.send("Invalid action. Use 'get' or 'set'.")

config_example()  # Call to initialize 