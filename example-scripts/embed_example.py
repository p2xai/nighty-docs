@nightyScript(
    name="Embed Example",
    author="thedorekaczynski",
    description="Demonstrates message sending with embeds",
    usage="<p>embed <title> | <content> [| <image_url>]"
)
def embed_example():
    """
    Embed Example
    ------------
    
    This script demonstrates how to send messages with embeds.
    It uses the forwardEmbedMethod to send rich embeds.
    
    COMMANDS:
    <p>embed <title> | <content> [| <image_url>] - Send an embed message
    
    EXAMPLES:
    <p>embed Hello | This is a test embed - Send a simple embed
    <p>embed Image | Check this out | https://example.com/image.jpg - Send an embed with an image
    
    NOTES:
    - The title, content, and image URL are separated by the | character
    - The image URL is optional
    - The embed is sent to the same channel as the command
    """
    
    @bot.command(name="embed", description="Send an embed message")
    async def embed_command(ctx, *, args: str):
        await ctx.message.delete()
        
        # Split the arguments by the | character
        parts = [part.strip() for part in args.split("|")]
        
        if len(parts) < 2:
            await ctx.send("Usage: `<p>embed <title> | <content> [| <image_url>]`")
            return
            
        title = parts[0]
        content = parts[1]
        image_url = parts[2] if len(parts) > 2 else None
        
        # Save current private setting and update it to False (disable private mode)
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            # Send the embed message
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=content,
                title=title,
                image=image_url
            )
        finally:
            # Restore the original private setting
            updateConfigData("private", current_private)
            
        # Send a confirmation message
       # await ctx.send("Embed sent!")

embed_example()  # Call to initialize 