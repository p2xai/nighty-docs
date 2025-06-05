@nightyScript(
    name="Webhook Example",
    author="thedorekaczynski",
    description="Demonstrates webhook integration",
    usage="<p>webhook set <url> OR <p>webhook send <message> OR <p>webhook status"
)
def webhook_example():
    """
    Webhook Example
    -------------
    
    This script demonstrates how to use webhooks to send messages.
    It allows you to set a webhook URL and send messages to it.
    
    COMMANDS:
    <p>webhook set <url> - Set the webhook URL
    <p>webhook send <message> - Send a message to the webhook
    <p>webhook status - Check if a webhook URL is set
    
    EXAMPLES:
    <p>webhook set https://discord.com/api/webhooks/... - Set the webhook URL
    <p>webhook send Hello, world! - Send a message to the webhook
    <p>webhook status - Check if a webhook URL is set
    
    NOTES:
    - The webhook URL is stored in the configuration
    - Messages are sent asynchronously to avoid blocking the main thread
    - The webhook URL must be a valid Discord webhook URL
    """
    
    import requests
    import asyncio
    from datetime import datetime
    
    # Configuration key for the webhook URL
    WEBHOOK_URL_KEY = "webhook_example_url"
    
    # Helper function for asynchronous webhook requests
    async def run_in_thread(func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    
    # Function to send a webhook message
    def send_webhook_message(content):
        webhook_url = getConfigData().get(WEBHOOK_URL_KEY)
        if not webhook_url:
            return False
            
        payload = {
            "content": content,
            "username": "Webhook Example",
            "avatar_url": "https://cdn.discordapp.com/embed/avatars/0.png"
        }
        
        try:
            response = requests.post(webhook_url, json=payload)
            return response.status_code == 204  # 204 indicates success
        except Exception as e:
            print(f"Webhook error: {str(e)}", type_="ERROR")
            return False
    
    @bot.command(name="webhook", description="Manage webhook integration")
    async def webhook_command(ctx, *, args: str):
        await ctx.message.delete()
        
        # Split the arguments
        parts = args.strip().split(maxsplit=1)
        if not parts:
            await ctx.send("Usage: `<p>webhook set <url>` OR `<p>webhook send <message>` OR `<p>webhook status`")
            return
            
        action = parts[0].lower()
        
        if action == "set":
            if len(parts) < 2:
                await ctx.send("Usage: `<p>webhook set <url>`")
                return
                
            url = parts[1]
            
            # Validate the URL (basic check)
            if not url.startswith("https"):
                await ctx.send("Invalid webhook URL. It should start with 'https'")
                return
                
            # Set the webhook URL
            updateConfigData(WEBHOOK_URL_KEY, url)
            await ctx.send("Webhook URL set.")
            
        elif action == "send":
            if len(parts) < 2:
                await ctx.send("Usage: `<p>webhook send <message>`")
                return
                
            message = parts[1]
            
            # Check if a webhook URL is set
            webhook_url = getConfigData().get(WEBHOOK_URL_KEY)
            if not webhook_url:
                await ctx.send("No webhook URL set. Use `<p>webhook set <url>` to set one.")
                return
                
            # Send a status message
            status_msg = await ctx.send("Sending message to webhook...")
            
            # Send the message to the webhook
            success = await run_in_thread(send_webhook_message, message)
            
            # Update the status message
            if success:
                await status_msg.edit(content="Message sent to webhook!")
            else:
                await status_msg.edit(content="Failed to send message to webhook.")
                
        elif action == "status":
            # Check if a webhook URL is set
            webhook_url = getConfigData().get(WEBHOOK_URL_KEY)
            if webhook_url:
                await ctx.send(f"Webhook URL is set: {webhook_url}")
            else:
                await ctx.send("No webhook URL set. Use `<p>webhook set <url>` to set one.")
                
        else:
            await ctx.send("Invalid action. Use 'set', 'send', or 'status'.")

webhook_example()  # Call to initialize 