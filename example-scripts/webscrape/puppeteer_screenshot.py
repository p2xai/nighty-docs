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
    - The Node.js code is embedded in this script and written to a temporary
      file at runtime.
    """
    import asyncio
    import discord
    import os
    from pathlib import Path
    import uuid

    import tempfile
    import textwrap

    JS_CODE = textwrap.dedent(
        """
        const fs = require('fs');
        const puppeteer = require('puppeteer');

        (async () => {
          const [url, output] = process.argv.slice(2);
          if (!url || !output) {
            console.error('Usage: node puppeteer_screenshot.js <url> <output>');
            process.exit(1);
          }
          const browser = await puppeteer.launch();
          try {
            const page = await browser.newPage();
            await page.goto(url, { waitUntil: 'networkidle2' });
            await page.screenshot({ path: output, fullPage: true });
          } catch (err) {
            console.error(err.toString());
            process.exit(1);
          } finally {
            await browser.close();
          }
        })();
        """
    )

    async def write_js_temp() -> Path:
        temp_js = Path(tempfile.gettempdir()) / f"puppshot_{uuid.uuid4().hex}.js"
        temp_js.write_text(JS_CODE)
        return temp_js

    async def run_puppeteer(url: str, out_file: Path) -> bool:
        js_file = await write_js_temp()
        try:
            proc = await asyncio.create_subprocess_exec(
                "node", str(js_file), url, str(out_file)
            )
            await proc.communicate()
            return proc.returncode == 0 and out_file.exists()
        finally:
            try:
                js_file.unlink()
            except OSError:
                pass

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