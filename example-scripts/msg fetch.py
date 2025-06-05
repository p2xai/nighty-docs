@nightyScript(
    name="Message Range Fetcher",
    author="thedorekaczynski",
    description="Fetches all messages between two given message IDs in a channel.",
    usage="<p>between <message_id_start> <message_id_end>"
)
def message_range_script():
    """
    MESSAGE RANGE FETCHER
    ---------------------
    
    This script allows you to fetch and display all messages between two specified message IDs in the same channel.
    
    COMMANDS:
    <p>between <start_id> <end_id> - Fetch messages between two message IDs
    
    EXAMPLES:
    <p>between 112233445566778899 998877665544332211 - Fetch all messages between the two given message IDs
    
    NOTES:
    - Both message IDs must be from the same channel.
    - The script fetches messages in chronological order.
    - Will include the messages at both endpoints.
    """
    
    import asyncio

    @bot.command(
        name="between",
        usage="<start_id> <end_id>",
        description="Fetch messages between two message IDs"
    )
    async def fetch_between(ctx, *, args: str):
        await ctx.message.delete()
        parts = args.strip().split()
        if len(parts) != 2:
            await ctx.send("Usage: `<p>between <start_id> <end_id>`")
            return
        
        try:
            start_id = int(parts[0])
            end_id = int(parts[1])
        except ValueError:
            await ctx.send("Both IDs must be valid integers.")
            return

        if start_id == end_id:
            await ctx.send("Start and end message IDs must be different.")
            return

        if start_id > end_id:
            start_id, end_id = end_id, start_id  # Ensure chronological order

        channel = ctx.channel
        all_messages = []

        try:
            async for message in channel.history(limit=None, after=discord.Object(id=start_id-1), before=discord.Object(id=end_id+1), oldest_first=True):
                all_messages.append(message)
        except Exception as e:
            await ctx.send(f"Error fetching messages: {str(e)}")
            return

        if not all_messages:
            await ctx.send("No messages found in the given range.")
            return

        content_lines = []
        for msg in all_messages:
            author = f"{msg.author.name}#{msg.author.discriminator}"
            timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            content = msg.content or "[No Text]"
            content_lines.append(f"**{author}** ({timestamp}): {content}")

        content = "\n".join(content_lines)

        chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
        for chunk in chunks:
            await ctx.send(chunk)

message_range_script()
