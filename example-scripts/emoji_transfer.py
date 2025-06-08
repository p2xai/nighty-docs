@nightyScript(
    name="Emoji Transfer",
    author="AutoGPT",
    description="Transfer emojis from one server to another with cooldowns and logging.",
    usage="<p>transferemojis <source_server_id> <target_server_id>"
)
def emoji_transfer():
    """
    EMOJI TRANSFER SCRIPT
    ---------------------

    Copies custom emojis from one guild to another.

    COMMANDS:
    <p>transferemojis <source_id> <target_id> - Copy all custom emojis from the source server to the target.

    NOTES:
    - The bot must be in both servers
    - Adds a short delay between uploads to avoid hitting rate limits.
    - Progress is logged to the console.
    """
    import aiohttp
    import asyncio
    from datetime import datetime

    SCRIPT_NAME = "Emoji Transfer"

    def script_log(message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{SCRIPT_NAME}] [{level}] {message}", type_=level)

    @bot.command(
        name="transferemojis",
        description="Transfer emojis from one server to another."
    )
    async def transfer_emojis(ctx, source_id: str, target_id: str):
        await ctx.message.delete()

        try:
            source_guild = bot.get_guild(int(source_id))
            target_guild = bot.get_guild(int(target_id))
        except ValueError:
            await ctx.send("Server IDs must be integers.")
            return

        if source_guild is None or target_guild is None:
            await ctx.send(
                "Could not find the specified servers. Make sure the bot is in both servers."
            )
            return

        script_log(
            f"Starting transfer from {source_guild.name} ({source_guild.id}) to {target_guild.name} ({target_guild.id}).",
            level="INFO",
        )

        transferred = 0
        async with aiohttp.ClientSession() as session:
            for emoji in source_guild.emojis:
                try:
                    async with session.get(str(emoji.url)) as resp:
                        img_bytes = await resp.read()

                    await target_guild.create_custom_emoji(name=emoji.name, image=img_bytes)
                    script_log(f"Uploaded {emoji.name}", level="SUCCESS")
                    transferred += 1
                except Exception as e:
                    script_log(f"Failed to upload {emoji.name}: {e}", level="ERROR")
                await asyncio.sleep(1)  # Cooldown between uploads

        script_log(f"Transferred {transferred} emojis.", level="SUCCESS")
        await ctx.send(f"Transferred {transferred} emojis from {source_guild.name} to {target_guild.name}.")

emoji_transfer()
