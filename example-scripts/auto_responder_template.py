@nightyScript(
    name="Hello Responder",
    author="AutoGPT",
    description="Automatically replies to greetings.",
    usage="No commands"
)
def script_function():
    """
    AUTO RESPONDER TEMPLATE
    -----------------------

    Replies to keywords in messages.

    TRIGGERS:
    When a user says "hello" or "hi", the bot responds with "Hello!".

    NOTES:
    - Demonstrates the auto-responder pattern (Section 6.2)
    - Consider filtering to specific channels or users to avoid spam
    - Without any check it responds to everyone in all servers.
      Adding a quick user ID filter keeps it targeted.
    """

    @bot.listen("on_message")
    async def hello_listener(message):
        TARGET_USER_ID = 839561905403068467
        if message.author.id == bot.user.id:
            return
        if message.author.id != TARGET_USER_ID:
            return
        content = message.content.lower()
        if "hello" in content or "hi" in content:
            await message.channel.send("Hello!", silent=True)

script_function()
