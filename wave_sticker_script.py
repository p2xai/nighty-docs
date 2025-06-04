@nightyScript(
    name="Wave Sticker",
    author="AutoGPT",
    description="Send the wave sticker.",
    usage="<p>wave"
)
def script_function():
    """
    WAVE STICKER SCRIPT
    -------------------

    Sends stickers on command.

    COMMANDS:
    <p>wave - Send the wave sticker
    <p>sticker <id> - Send any sticker by ID

    EXAMPLES:
    <p>wave - Bot replies with the wave sticker

    NOTES:
    - Sticker ID: 749054660769218631
    - Attempts to use the cached sticker first, then fetches if needed
    - Works with custom stickers as long as the bot can access them
    """
    STICKER_ID = 749054660769218631

    @bot.command(name="wave", description="Send the wave sticker.")
    async def wave_cmd(ctx):
        await ctx.message.delete()
        try:
            sticker = bot.get_sticker(STICKER_ID)
            if not sticker:
                sticker = await bot.fetch_sticker(STICKER_ID)
            await ctx.send(stickers=[sticker])
        except Exception as e:
            await ctx.send(f"Failed to send sticker: {e}")

    @bot.command(name="sticker", description="Send any sticker by ID.")
    async def custom_sticker_cmd(ctx, sticker_id: str):
        await ctx.message.delete()
        try:
            sid = int(sticker_id)
        except ValueError:
            await ctx.send("Sticker ID must be an integer.")
            return
        try:
            sticker = bot.get_sticker(sid)
            if not sticker:
                sticker = await bot.fetch_sticker(sid)
            await ctx.send(stickers=[sticker])
        except Exception as e:
            await ctx.send(f"Failed to send sticker: {e}")

script_function()
