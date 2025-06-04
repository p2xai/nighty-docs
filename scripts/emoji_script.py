@nightyScript(
    name="Emoji",
    author="AutoGPT",
    description="Send custom emojis by ID.",
    usage="<p>emoji <id>"
)
def script_function():
    """
    EMOJI SCRIPT
    -----------

    Sends custom emojis on command.

    COMMANDS:
    <p>emoji <id> - Send any custom emoji by ID

    EXAMPLES:
    <p>emoji 123456789012345678 - Bot replies with the specified emoji

    NOTES:
    - The emoji ID must come from a guild where the bot has access
    - Uses `bot.get_emoji` and falls back to sending the raw emoji string
    - Messages are sent with `silent=True` so no mention is triggered
    """

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
            if emoji:
                await ctx.send(str(emoji), silent=True)
            else:
                await ctx.send(f"<:emoji:{eid}>", silent=True)
        except Exception as e:
            await ctx.send(f"Failed to send emoji: {e}")

script_function()
