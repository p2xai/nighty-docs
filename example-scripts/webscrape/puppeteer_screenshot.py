@nightyScript(
    name="Puppeteer Screenshot",
    author="AutoGPT",
    description="Capture a website screenshot using Node.js Puppeteer",
    usage="<p>puppshot <url>"
)
def puppeteer_screenshot():
    """
    Puppeteer Screenshot
    --------------------

    Captures a screenshot of a webpage using Node.js Puppeteer.

    COMMANDS:
    <p>puppshot <url> - Capture the given URL as an image

    EXAMPLE:
    <p>puppshot https://example.com

    NOTES:
    - Requires Node.js and the `puppeteer` package.
    - Install with: `npm install puppeteer`
    - Python calls a Node script to generate the screenshot.
    """
    import asyncio
    import discord
    import os
    from pathlib import Path
    import uuid

    JS_FILE = Path(__file__).with_name("puppeteer_screenshot.js")

    async def run_puppeteer(url: str, out_file: Path) -> bool:
        proc = await asyncio.create_subprocess_exec(
            "node", str(JS_FILE), url, str(out_file)
        )
        await proc.communicate()
        return proc.returncode == 0 and out_file.exists()

    @bot.command(name="puppshot", aliases=["pshot"], description="Screenshot a webpage using Puppeteer")
    async def puppshot_command(ctx, *, url: str):
        await ctx.message.delete()
        url = url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        temp_file = Path(os.getcwd()) / f"puppshot_{uuid.uuid4().hex}.png"
        status_msg = await ctx.send(f"Capturing screenshot for {url}...")
        success = await run_puppeteer(url, temp_file)
        if not success:
            await status_msg.edit(content="Failed to capture screenshot.")
            return
        file = discord.File(str(temp_file), filename="screenshot.png")
        await status_msg.delete()
        await ctx.send(file=file)
        try:
            temp_file.unlink()
        except OSError:
            pass

puppeteer_screenshot()
