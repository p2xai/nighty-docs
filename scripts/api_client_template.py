@nightyScript(
    name="Cat Fact",
    author="AutoGPT",
    description="Fetch a random cat fact using an API.",
    usage="<p>catfact"
)
def script_function():
    """
    API CLIENT TEMPLATE
    -------------------

    Demonstrates how to fetch data from an external API.

    COMMANDS:
    <p>catfact - Fetch a random cat fact

    NOTES:
    - Uses `aiohttp` to perform an HTTP GET request
    - Shows JSON parsing and simple error handling
    - For APIs requiring keys, store them in config files
    """
    import aiohttp

    @bot.command(name="catfact", description="Fetch a random cat fact.")
    async def catfact_cmd(ctx):
        await ctx.message.delete()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://catfact.ninja/fact") as resp:
                    data = await resp.json()
                    fact = data.get("fact", "No fact available.")
                    await ctx.send(fact, silent=True)
        except Exception as e:
            await ctx.send(f"Failed to fetch cat fact: {e}")

script_function()
