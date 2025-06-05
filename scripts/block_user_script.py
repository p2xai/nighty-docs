@nightyScript(
    name="Block User",
    author="AutoGPT",
    description="Block a user by ID or mention.",
    usage="<p>block <user>"
)
def script_function():
    """
    BLOCK USER SCRIPT
    -----------------

    Provides a command to block a specified user.

    COMMANDS:
    <p>block <user> - Block the given user by ID or mention

    EXAMPLES:
    <p>block 123456789012345678
    <p>block @SomeUser

    NOTES:
    - Uses `User.block()` from discord.py-self
    - The command expects a user ID or mention
    """

    @bot.command(name="block", description="Block a user by ID or mention.")
    async def block_cmd(ctx, *, target: str):
        await ctx.message.delete()
        try:
            if target.startswith("<@") and target.endswith(">"):
                uid = int(target.strip("<@!>"))
            else:
                uid = int(target)
        except ValueError:
            await ctx.send("Invalid user ID or mention.")
            return

        try:
            user = bot.get_user(uid)
            if user is None:
                user = await bot.fetch_user(uid)
            await user.block()
            await ctx.send(f"User ({user.mention}) blocked.")
        except Exception as e:
            await ctx.send(f"Failed to block user: {e}")

script_function()
