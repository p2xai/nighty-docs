@nightyScript(
    name="Async Example",
    author="thedorekaczynski",
    description="Demonstrates asynchronous operations",
    usage="<p>async <url> OR <p>async sleep <seconds>"
)
def async_example():
    """
    Async Example
    ------------
    
    This script demonstrates how to use asynchronous operations.
    It includes examples of making HTTP requests and using sleep.
    
    COMMANDS:
    <p>async <url> - Make an HTTP request to the specified URL
    <p>async sleep <seconds> - Sleep for the specified number of seconds
    
    EXAMPLES:
    <p>async https://example.com - Make an HTTP request to example.com
    <p>async sleep 5 - Sleep for 5 seconds
    
    NOTES:
    - HTTP requests are made using aiohttp
    - Sleep is implemented using asyncio.sleep
    - All operations are non-blocking
    """
    
    import aiohttp
    import asyncio
    
    @bot.command(name="async", description="Perform asynchronous operations")
    async def async_command(ctx, *, args: str):
        await ctx.message.delete()
        
        # Split the arguments
        parts = args.strip().split(maxsplit=1)
        if not parts:
            await ctx.send("Usage: `<p>async <url>` OR `<p>async sleep <seconds>`")
            return
            
        action = parts[0].lower()
        
        if action == "sleep":
            if len(parts) < 2:
                await ctx.send("Usage: `<p>async sleep <seconds>`")
                return
                
            try:
                seconds = float(parts[1])
                if seconds < 0:
                    await ctx.send("Sleep time cannot be negative.")
                    return
                    
                # Send a status message
                status_msg = await ctx.send(f"Sleeping for {seconds} seconds...")
                
                # Sleep for the specified number of seconds
                await asyncio.sleep(seconds)
                
                # Update the status message
                await status_msg.edit(content=f"Slept for {seconds} seconds.")
                
            except ValueError:
                await ctx.send("Invalid sleep time. Please provide a number.")
                
        else:
            # Treat the action as a URL
            url = args.strip()
            
            # Validate the URL (basic check)
            if not url.startswith(("http://", "https://")):
                await ctx.send("Invalid URL. It should start with 'http://' or 'https://'")
                return
                
            # Send a status message
            status_msg = await ctx.send(f"Making HTTP request to {url}...")
            
            try:
                # Make an HTTP request using aiohttp
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            # Get the response content
                            content = await response.text()
                            
                            # Truncate the content if it's too long
                            if len(content) > 1000:
                                content = content[:1000] + "..."
                                
                            # Update the status message
                            await status_msg.edit(content=f"Response from {url} (Status: {response.status}):\n```\n{content}\n```")
                        else:
                            # Update the status message with the error
                            await status_msg.edit(content=f"Error: HTTP {response.status}")
                            
            except Exception as e:
                # Update the status message with the error
                await status_msg.edit(content=f"Error: {str(e)}")

async_example()  # Call to initialize 