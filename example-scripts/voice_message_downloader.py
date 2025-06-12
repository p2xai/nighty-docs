@nightyScript(
    name="Voice Message Downloader",
    author="AutoGPT",
    description="Download voice message audio by message link or ID.",
    usage="<p>voicedl <message_id_or_link>"
)
def voice_message_downloader():
    """
    VOICE MESSAGE DOWNLOADER
    -----------------------

    Fetch the audio file from a Discord voice message.

    COMMANDS:
    <p>voicedl <message_id_or_link> - Download the voice message as a file

    EXAMPLES:
    <p>voicedl 112233445566778899
    <p>voicedl https://discord.com/channels/123/456/789

    NOTES:
    - The message must be in a channel the bot can access
    - Works with voice messages that are sent as audio attachments
    """
    import re
    import discord

    MESSAGE_URL_RE = re.compile(
        r"https?://(?:ptb\\.|canary\\.)?discord(?:app)?\\.com/channels/(\\d+)/(\\d+)/(\\d+)"
    )

    def parse_reference(ref: str):
        match = MESSAGE_URL_RE.match(ref)
        if match:
            _, channel_id, message_id = match.groups()
            return int(channel_id), int(message_id)
        try:
            return None, int(ref)
        except ValueError:
            return None, None

    @bot.command(name="voicedl", description="Download a voice message by link or ID")
    async def voice_dl(ctx, *, reference: str):
        await ctx.message.delete()

        channel = ctx.channel
        channel_id, message_id = parse_reference(reference.strip())
        if message_id is None:
            await ctx.send("Invalid message ID or link.")
            return
        if channel_id:
            channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
            if channel is None:
                await ctx.send("Channel not found or inaccessible.")
                return
        try:
            message = await channel.fetch_message(message_id)
        except Exception as e:
            await ctx.send(f"Failed to fetch message: {e}")
            return

        voice_attachment = None
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("audio"):
                voice_attachment = attachment
                break
            if attachment.filename.lower().endswith((".ogg", ".mp3", ".wav")):
                voice_attachment = attachment
                break

        if voice_attachment is None:
            await ctx.send("No voice attachment found in that message.")
            return

        try:
            voice_file = await voice_attachment.to_file()
            await ctx.send(file=voice_file)
        except Exception as e:
            await ctx.send(f"Failed to send audio file: {e}")

voice_message_downloader()
