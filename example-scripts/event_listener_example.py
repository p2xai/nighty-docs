@nightyScript(
    name="Event Listener Example",
    author="thedorekaczynski",
    description="Demonstrates the use of event listeners",
    usage="<p>event on/off OR <p>event status"
)
def event_listener_example():
    """
    Event Listener Example
    -------------------
    
    This script demonstrates how to use event listeners.
    It responds to messages containing specific keywords.
    
    COMMANDS:
    <p>event on/off - Enable or disable the event listener
    <p>event status - Check if the event listener is enabled
    
    EXAMPLES:
    <p>event on - Enable the event listener
    <p>event off - Disable the event listener
    <p>event status - Check if the event listener is enabled
    
    NOTES:
    - The event listener responds to messages containing 'hello', 'hi', or 'hey'
    - The event listener is enabled by default
    - The event listener ignores messages from the bot itself
    """
    
    # Configuration key for enabling/disabling the event listener
    ENABLED_KEY = "event_listener_enabled"
    
    # Initialize the configuration if it doesn't exist
    if getConfigData().get(ENABLED_KEY) is None:
        updateConfigData(ENABLED_KEY, True)  # Enabled by default
    
    @bot.command(name="event", description="Enable or disable the event listener")
    async def event_command(ctx, *, args: str):
        await ctx.message.delete()
        
        args = args.strip().lower()
        
        if args == "on":
            updateConfigData(ENABLED_KEY, True)
            await ctx.send("Event listener enabled.")
            
        elif args == "off":
            updateConfigData(ENABLED_KEY, False)
            await ctx.send("Event listener disabled.")
            
        elif args == "status":
            enabled = getConfigData().get(ENABLED_KEY, True)
            status = "enabled" if enabled else "disabled"
            await ctx.send(f"Event listener is {status}.")
            
        else:
            await ctx.send("Usage: `<p>event on/off` OR `<p>event status`")
    
    @bot.listen("on_message")
    async def message_handler(message):
        # Ignore messages from the bot itself
        if message.author.id == bot.user.id:
            return
            
        # Check if the event listener is enabled
        if not getConfigData().get(ENABLED_KEY, True):
            return
            
        # Check if the message contains any of the keywords
        content = message.content.lower()
        keywords = ["hello", "hi", "hey"]
        
        for keyword in keywords:
            if keyword in content:
                # Send a response
                await message.channel.send(f"Hello, {message.author.mention}! I noticed you said '{keyword}'.")
                break  # Only respond once per message

event_listener_example()  # Call to initialize 