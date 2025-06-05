@nightyScript(
    name="Delete Logger",
    author="AutoGPT",
    description="Log deleted messages to a channel.",
    usage="No commands"
)
def script_function():
    """
    EVENT LOGGER TEMPLATE
    ---------------------

    Logs message deletions using `forwardEmbedMethod`.

    CONFIG:
    Set `LOG_CHANNEL_ID` to the ID of your log channel.

    NOTES:
    - Illustrates the event logger pattern (Section 6.3)
    - Uses embed-style logging for clarity
    """

    LOG_CHANNEL_ID = 123456789012345678  # Replace with your log channel ID

    @bot.listen("on_message_delete")
    async def delete_logger(message):
        try:
            await forwardEmbedMethod(
                channel_id=LOG_CHANNEL_ID,
                content=(f"**Message deleted**\n"
                         f"User: {message.author}\n"
                         f"Channel: {message.channel}\n"
                         f"Content: {message.content}")
            )
        except Exception as e:
            print(f"Failed to log message: {e}")

script_function()
