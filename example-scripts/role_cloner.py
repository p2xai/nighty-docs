@nightyScript(
    name="Role Cloner",
    author="AutoGPT",
    description="Clone a role and its icon to another server.",
    usage="<p>clonerole <role_id> <target_server_id>"
)
def role_cloner():
    """
    ROLE CLONER
    ------------

    Copy a role, including its icon, to another server.

    COMMANDS:
    <p>clonerole <role_id> <target_server_id> - Duplicate the role to the target server.

    EXAMPLES:
    <p>clonerole 123456789012345678 987654321098765432

    NOTES:
    - The bot must be in both servers and have permissions to manage roles.
    - The role ID can be from any server the bot can see; the script will search all guilds.
    - Role position is not preserved when cloning.
    - The role icon is copied if one exists.
    """

    @bot.command(name="clonerole", description="Clone a role to another server.")
    async def clone_role_cmd(ctx, role_id: str, target_guild_id: str):
        await ctx.message.delete()
        try:
            rid = int(role_id)
            gid = int(target_guild_id)
        except ValueError:
            await ctx.send("IDs must be integers.")
            return

        source_role = None
        for guild in bot.guilds:
            source_role = guild.get_role(rid)
            if source_role:
                break
        if source_role is None:
            await ctx.send(f"Role with ID {rid} not found.")
            return

        target_guild = bot.get_guild(gid)
        if target_guild is None:
            await ctx.send(f"Target server with ID {gid} not found.")
            return

        icon_bytes = None
        if source_role.icon:
            try:
                icon_bytes = await source_role.icon.read()
            except Exception as e:
                await ctx.send(f"Could not fetch role icon: {e}")
                icon_bytes = None

        try:
            await target_guild.create_role(
                name=source_role.name,
                permissions=source_role.permissions,
                colour=source_role.colour,
                hoist=source_role.hoist,
                mentionable=source_role.mentionable,
                icon=icon_bytes,
            )
            await ctx.send(f"Cloned role '{source_role.name}' to {target_guild.name}.")
        except Exception as e:
            await ctx.send(f"Failed to clone role: {e}")

role_cloner()
