@nightyScript(
    name="Mass Unban",
    author="AutoGPT",
    description="Unban all users in the server with a delay between each unban.",
    usage="<p>massunban"
)
def mass_unban_script():
    """
    MASS UNBAN SCRIPT
    -----------------

    Unban every banned user in the current Discord server.

    COMMANDS:
    <p>massunban - Unban all users with a 0.7 second delay between actions

    EXAMPLES:
    <p>massunban - Remove all bans from the server the command is used in

    NOTES:
    - Requires the `ban_members` permission in the server.
    - Uses `ctx.guild.bans()` to fetch the ban list.
    - Implements rate limiting with `asyncio.sleep(0.7)` between unbans.
    """

    import asyncio

    @bot.command(name="massunban", description="Unban every user in the server")
    async def mass_unban_cmd(ctx):
        await ctx.message.delete()
        guild = ctx.guild
        if guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        status = await ctx.send(f"Fetching bans for {guild.name}...")
        try:
            bans = await guild.bans()
        except Exception as e:
            await status.edit(content=f"Failed to fetch bans: {e}")
            return

        if not bans:
            await status.edit(content="No banned users found.")
            return

        await status.edit(content=f"Unbanning {len(bans)} user(s)...")

        unbanned = 0
        for ban_entry in bans:
            user = ban_entry.user
            try:
                print(
                    f"Attempting to unban {user.name}#{user.discriminator} ({user.id})",
                    type_="INFO",
                )
                await guild.unban(user)
                unbanned += 1
                print(
                    f"Successfully unbanned {user.name}#{user.discriminator} ({user.id})",
                    type_="SUCCESS",
                )
                await asyncio.sleep(0.7)
            except Exception as e:
                print(
                    f"Failed to unban {user.name}#{user.discriminator} ({user.id}): {e}",
                    type_="ERROR",
                )
                await ctx.send(f"Failed to unban {user}: {e}")

        await status.edit(content=f"Unbanned {unbanned} user(s) from {guild.name}.")

mass_unban_script()
