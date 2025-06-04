@nightyScript(
    name="Wave Emoji",
    author="AutoGPT",
    description="Send the wave emoji or any custom emoji by ID.",
    usage="<p>waveemoji"
)
def script_function():
    """
    WAVE EMOJI SCRIPT
    -----------------

    Sends custom emojis on command.

    COMMANDS:
    <p>waveemoji - Send the wave emoji
    <p>emoji <id> - Send any custom emoji by ID

    EXAMPLES:
    <p>waveemoji - Bot replies with the wave emoji

    NOTES:
    - Emoji ID: 123456789012345678
    - Attempts to use the cached emoji first, then fetches if needed
    - Works with custom emojis the bot can access
    """
    EMOJI_ID = 123456789012345678

    @bot.command(name="waveemoji", description="Send the wave emoji.")
    async def waveemoji_cmd(ctx):
        await ctx.message.delete()
        try:
            emoji = bot.get_emoji(EMOJI_ID)
            if not emoji:
                emoji = await bot.fetch_emoji(EMOJI_ID)
            await ctx.send(str(emoji))
        except Exception as e:
            await ctx.send(f"Failed to send emoji: {e}")

    @bot.command(name="emoji", description="Send any custom emoji by ID.")
    async def custom_emoji_cmd(ctx, emoji_id: str):
        await ctx.message.delete()
        try:
            eid = int(emoji_id)
        except ValueError:
            await ctx.send("Emoji ID must be an integer.")
            return
        try:
            emoji = bot.get_emoji(eid)
            if not emoji:
                emoji = await bot.fetch_emoji(eid)
            await ctx.send(str(emoji))
        except Exception as e:
            await ctx.send(f"Failed to send emoji: {e}")

script_function()
