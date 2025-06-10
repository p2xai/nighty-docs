@nightyScript(
    name="Website Screenshot",
    author="AutoGPT",
    description="Capture a screenshot of a website and send it as an image",
    usage="<p>screenshot <url>"
)
def website_screenshot():
    """
    WEBSITE SCREENSHOT SCRIPT
    -------------------------

    Captures screenshots of websites using the public thum.io service.

    COMMANDS:
    <p>screenshot <url> - Capture a screenshot of the specified URL

    EXAMPLE:
    <p>screenshot https://example.com

    NOTES:
    - Uses https://image.thum.io to generate screenshots
    - Adds "http://" if no scheme is provided
    - Sends the screenshot as a file attachment in the channel
    """
    import aiohttp
    import io
    import discord

    async def fetch_screenshot_bytes(target_url: str):
        screenshot_url = f"https://image.thum.io/get/png/{target_url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(screenshot_url) as resp:
                if resp.status != 200:
                    return None
                return await resp.read()

    @bot.command(name="screenshot", aliases=["shot"], description="Capture a website screenshot")
    async def screenshot_command(ctx, *, url: str):
        await ctx.message.delete()
        url = url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        status_msg = await ctx.send(f"Fetching screenshot for {url}...")
        data = await fetch_screenshot_bytes(url)
        if not data:
            await status_msg.edit(content="Failed to fetch screenshot.")
            return
        file = discord.File(io.BytesIO(data), filename="screenshot.png")
        await status_msg.delete()
        await ctx.send(file=file)

website_screenshot()
