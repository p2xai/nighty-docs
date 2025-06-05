@nightyScript(
    name="Rapid Message Cleaner v1.0",
    author="thedorekaczynski",
    description="Rapidly deletes your messages sent in the past 3 minutes",
    usage="<p>clean - Starts the cleanup process"
)
def message_cleaner():
    """
    RAPID MESSAGE CLEANER SCRIPT
    -------------------------
    
    This script provides a quick way to clean up your recent messages in a channel.
    It automatically finds and deletes messages you've sent in the past 3 minutes.
    
    FEATURES:
    - Rapid message deletion
    - Only deletes your own messages
    - Status updates during cleanup
    - Rate-limited to avoid API throttling
    - Error handling for failed deletions
    - Auto-deleting status messages
    
    COMMANDS:
    <p>clean    - Start cleaning messages from the past 3 minutes
    
    EXAMPLE USAGE:
    <p>clean    - "🧹 Starting message cleanup..."
                - "✅ Cleanup complete! Deleted 5 messages from the past minute."
    
    BEHAVIOR:
    - Searches last 100 messages in the channel
    - Only deletes messages from past 3 minutes
    - 0.5 second delay between deletions
    - Status message auto-deletes after 5 seconds
    
    NOTES:
    - Only affects your own messages
    - Status messages are temporary
    - Safe to use in any channel
    """
    import asyncio
    import time
    from datetime import datetime, timedelta
    
    @bot.command(name="clean", description="Rapidly delete messages sent in the past 3 minutes")
    async def clean_command(ctx, *, args: str = ""):
        await ctx.message.delete()  # Delete the command message
        
        # Always use the channel where the command was sent
        channel = ctx.channel
            
        status_msg = await ctx.send("🧹 Starting message cleanup...")
        
        try:
            # Calculate the cutoff time (3 minutes ago)
            current_time = time.time()
            three_minutes_ago_ts = current_time - 180  # 180 seconds = 3 minutes
            
            deleted_count = 0
            
            # Get messages in channel and filter for our own messages in the past 3 minutes
            async for message in channel.history(limit=100):
                # Skip the status message
                if message.id == status_msg.id:
                    continue
                    
                # Only delete our own messages
                if message.author.id == bot.user.id:
                    # Convert message timestamp to UNIX timestamp for comparison
                    msg_ts = message.created_at.timestamp()
                    
                    # Check if message is within the time frame
                    if msg_ts > three_minutes_ago_ts:
                        try:
                            await message.delete()
                            deleted_count += 1
                            # Wait 0.5 seconds between deletions to avoid rate limits
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Error deleting message: {str(e)}", type_="WARNING")
            
            # Update status message with results
            await status_msg.edit(content=f"✅ Cleanup complete! Deleted {deleted_count} messages from the past 3 minutes.")
            
            # Delete status message after 5 seconds
            await asyncio.sleep(5)
            try:
                await status_msg.delete()
            except:
                pass
                
        except Exception as e:
            print(f"Error in clean command: {str(e)}", type_="ERROR")
            await status_msg.edit(content=f"❌ Error during cleanup: {str(e)}")

message_cleaner()  # Initialize the script