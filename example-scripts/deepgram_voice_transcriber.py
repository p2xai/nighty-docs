@nightyScript(
    name="Deepgram Voice Transcriber",
    author="AutoGPT",
    description="Transcribe Discord voice messages using Deepgram",
    usage="<p>transcribe <message_id_or_link> OR <p>deepgramkey <api_key>"
)
def deepgram_voice_transcriber():
    """
    DEEPGRAM VOICE TRANSCRIBER
    -------------------------

    Downloads a voice message attachment and sends it to the Deepgram API
    for transcription.

    COMMANDS:
    <p>transcribe <message_id_or_link> - Transcribe a voice message
    <p>deepgramkey <api_key> - Set the Deepgram API key

    EXAMPLES:
    <p>transcribe https://discord.com/channels/123/456/789
    <p>deepgramkey dg_yourkey

    NOTES:
    - Requires the `requests` package. Install with: `pip install requests`
    - The API key is stored in the script configuration.
    - Only messages in accessible channels can be fetched.
    """

    import re
    import asyncio
    import requests

    MESSAGE_URL_RE = re.compile(
        r"https?://(?:ptb\\.|canary\\.)?discord(?:app)?\\.com/channels/(\\d+)/(\\d+)/(\\d+)"
    )

    async def run_in_thread(func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    def parse_reference(ref: str):
        match = MESSAGE_URL_RE.match(ref)
        if match:
            _, channel_id, message_id = match.groups()
            return int(channel_id), int(message_id)
        try:
            return None, int(ref)
        except ValueError:
            return None, None

    def transcribe_audio(api_key: str, audio_bytes: bytes) -> str | None:
        url = "https://api.deepgram.com/v1/listen"
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/octet-stream",
        }
        try:
            resp = requests.post(url, headers=headers, data=audio_bytes)
            resp.raise_for_status()
            data = resp.json()
            return (
                data.get("results", {})
                .get("channels", [{}])[0]
                .get("alternatives", [{}])[0]
                .get("transcript")
            )
        except Exception as e:
            print(f"Deepgram API error: {e}", type_="ERROR")
            return None

    API_KEY_CONFIG = "deepgram_api_key"

    @bot.command(name="deepgramkey", description="Set Deepgram API key")
    async def set_key(ctx, *, key: str):
        await ctx.message.delete()
        updateConfigData(API_KEY_CONFIG, key.strip())
        await ctx.send("Deepgram API key updated.")

    @bot.command(name="transcribe", description="Transcribe a voice message")
    async def transcribe_cmd(ctx, *, reference: str):
        await ctx.message.delete()
        api_key = getConfigData().get(API_KEY_CONFIG)
        if not api_key:
            await ctx.send("No API key set. Use `<p>deepgramkey <api_key>`. ")
            return

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

        status_msg = await ctx.send("Transcribing voice message...")
        audio_bytes = await voice_attachment.read()
        transcript = await run_in_thread(transcribe_audio, api_key, audio_bytes)
        if transcript:
            await status_msg.edit(content=f"Transcription:\n```{transcript}```")
        else:
            await status_msg.edit(content="Failed to transcribe the audio.")


deepgram_voice_transcriber()
