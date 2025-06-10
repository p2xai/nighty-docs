@nightyScript(
    name="Role Icon Grabber",
    author="AutoGPT",
    description="Fetch role icons and send them as images.",
    usage="<p>roleicon <role_id> OR <p>roleicons [server_id]"
)
def role_icon_grabber():
    """
    ROLE ICON GRABBER
    -----------------

    Fetch role icon images from servers and send them in chat.

    COMMANDS:
    <p>roleicon <role_id> - Send the icon for the specified role
    <p>roleicons [server_id] - Send all role icons from the current or specified server

    EXAMPLES:
    <p>roleicon 123456789012345678
    <p>roleicons
    <p>roleicons 987654321098765432

    NOTES:
    - The bot must be in the server containing the roles
    - Uses aiohttp to download icon images
    """
    import aiohttp
    import io

    async def fetch_icon_bytes(url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                return await resp.read()

    @bot.command(name="roleicon", description="Send a role's icon by ID or mention")
    async def single_role_icon(ctx, role_id: str):
        await ctx.message.delete()
        role_id = role_id.strip("<@&>")
        try:
            rid = int(role_id)
        except ValueError:
            await ctx.send("Role ID must be an integer or mention.")
            return

        role = None
        if ctx.guild:
            role = ctx.guild.get_role(rid)
        if role is None:
            for guild in bot.guilds:
                role = guild.get_role(rid)
                if role:
                    break
        if role is None:
            await ctx.send(f"Role {rid} not found.")
            return
        if not role.icon:
            await ctx.send("This role has no icon.")
            return
        data = await fetch_icon_bytes(str(role.icon.url))
        if not data:
            await ctx.send("Failed to fetch the role icon.")
            return
        file = discord.File(io.BytesIO(data), filename=f"{role.name}.png")
        await ctx.send(file=file)

    @bot.command(name="roleicons", description="Send all role icons in a server")
    async def all_role_icons(ctx, server_id: str = None):
        await ctx.message.delete()
        guild = ctx.guild
        if server_id:
            try:
                gid = int(server_id)
                guild = bot.get_guild(gid)
            except ValueError:
                await ctx.send("Server ID must be an integer.")
                return
        if guild is None:
            await ctx.send("Server not found or bot not in server.")
            return
        sent = 0
        for role in guild.roles:
            if role.icon:
                data = await fetch_icon_bytes(str(role.icon.url))
                if data:
                    file = discord.File(io.BytesIO(data), filename=f"{role.name}.png")
                    await ctx.send(file=file, content=f"Role: {role.name}")
                    sent += 1
        if sent == 0:
            await ctx.send("No role icons found.")
        else:
            await ctx.send(f"Sent {sent} role icons from {guild.name}.")

role_icon_grabber()
