@nightyScript(
    name="Server Analytics",
    author="thedorekaczynski",
    description="Discord server member tracking and analytics system with growth trends",
    usage="""<p>analytics snapshot - Take a server snapshot
<p>analytics report - Generate a server analytics report
<p>analytics clear - Clear analytics data
<p>analytics status - Show analytics collection status
<p>analytics members - Show member count history graph
<p>analytics trend - Show member growth trend analysis
<p>analytics compare <days> - Compare server stats between two time periods
<p>analytics export - Export analytics data to a text file
<p>analytics auto <on/off> - Toggle automatic daily snapshots
<p>analytics retention [days] - Set snapshot data retention period
<p>analytics interval [hours] - Set auto-snapshot interval
<p>a <subcommand> - Shorthand for analytics command (same functionality)
<p>a ss - Short command for taking a snapshot
<p>a timezone <zone> - Set your preferred timezone (EST, PST, etc.)"""
)
def server_analytics():
    """
    SERVER ANALYTICS SCRIPT
    ---------------------
    
    Advanced Discord server member tracking and analytics with growth prediction.
    
    FEATURES:
    - Member count and demographics tracking
    - Server growth analysis with trends and rates
    - Multi-server support (separate data per server)
    - 30-day data retention with data export

    - Configurable timezone display
    - Automatic daily snapshots (optional)
    - Growth trend analysis and predictions
    - Server comparison between time periods
    - Data export functionality
    
    COMMANDS:
    <p>analytics snapshot     - Take an immediate snapshot
                             Shows members, channels, and timestamp
    <p>analytics report      - Generate detailed analytics report
                             Includes member stats, channels, roles, and growth
    <p>analytics clear      - Clear analytics data
                             Resets all stored data
    <p>analytics status     - Show analytics collection status
                             Displays snapshot count and latest data
    <p>analytics members    - Show member count history graph
                             Displays last 5 snapshots with trends and timestamps
    <p>analytics trend      - Show member growth trend analysis
                             Analyzes growth patterns and shows predictions
    <p>analytics compare <days> - Compare server stats between two time periods
                             Default compares current with 7 days ago
    <p>analytics export     - Export analytics data to a text file
                             Creates a downloadable record of your data
    <p>analytics auto <on/off> - Toggle automatic daily snapshots
                             Enables or disables automatic data collection
    <p>analytics retention [days] - Set how long snapshot data is kept (in days)
    <p>analytics interval [hours] - Set the interval for automatic snapshots
    <p>a ss                 - Short command for taking a snapshot
    <p>a timezone <zone>    - Set your preferred timezone (EST, PST, etc.)
    
    EXAMPLE OUTPUTS:
    Snapshot: 
     New Snapshot
    Server: Your Server
    Members: 3,495
    Channels: 96
    Time: 12:00:00 UTC
    
    Report Sections:
    -  Member Statistics (total, bots, humans)
    -  Channel Information (text, voice, categories)
    -  Role Count
    -  Growth Analysis
    
    Members Graph Example:
     Member Count History - Server Name 

    Apr 05, 06:47 PM EST
    Members: 3,495 (+5) 

    Apr 05, 05:30 PM EST
    Members: 3,490 (+2) 
    
    DATA STORAGE:
    - Base Directory: /json/server_member_tracking/<server_id>/
    - Files per server:
      • member_snapshots.json - Server member snapshots and metrics
      • analytics_config.json - Server-specific configuration
    
    NOTES:
    - Snapshots can be taken manually via command or automatically daily
    - Data is retained for 30 days
    - Each server has its own separate data storage
    - All timestamps are in UTC by default but displayed in your chosen timezone
    - Numbers are formatted with commas for readability
    - Safe to use alongside other scripts
    """
    from pathlib import Path
    import json

    BASE_DIR = Path(getScriptsPath()) / "json" / "server_member_tracking"
    import asyncio
    import re
    from pathlib import Path
    from datetime import datetime, timedelta
    from collections import defaultdict
    import time
    import random
    import math

    # Constants
    DEFAULT_AUTO_SNAPSHOT_INTERVAL_HOURS = 20
    DATA_RETENTION_DAYS = 90
    
    AUTO_SNAPSHOT_CONFIG_KEY = "server_analytics_auto_snapshot"
    LAST_AUTO_SNAPSHOT_KEY = "server_analytics_last_auto"
    
    # Timezone configuration
    TIMEZONE_CONFIG_KEY = "server_analytics_timezone"
    DEFAULT_TIMEZONE = "UTC"
    
    # Timezone offsets (in hours from UTC)
    TIMEZONE_OFFSETS = {
    "UTC": 0,
    "EST": -4,  # Eastern Standard Time (adjusted to match current EDT)
    "EDT": -4,  # Eastern Daylight Time
    "CST": -6,  # Central Standard Time
    "CDT": -5,  # Central Daylight Time
    "MST": -7,  # Mountain Standard Time
    "MDT": -6,  # Mountain Daylight Time
    "PST": -8,  # Pacific Standard Time
    "PDT": -7,  # Pacific Daylight Time
    "AKST": -9, # Alaska Standard Time
    "AKDT": -8, # Alaska Daylight Time
    "HST": -10, # Hawaii Standard Time
    "AEST": 10, # Australian Eastern Standard Time
    "AEDT": 11, # Australian Eastern Daylight Time
    "GMT": 0,   # Greenwich Mean Time
    "BST": 1,   # British Summer Time
    "CET": 1,   # Central European Time
    "CEST": 2,  # Central European Summer Time
    "JST": 9,   # Japan Standard Time
    "IST": 5.5, # India Standard Time (note: "IST" can also mean Irish Standard Time)
    }

    # Ensure base directory exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    def get_server_dir(guild_id):
        """Get the directory for a specific server's data"""
        server_dir = BASE_DIR / str(guild_id)
        server_dir.mkdir(parents=True, exist_ok=True)
        return server_dir

    def get_server_files(guild_id):
        """Get file paths for a specific server's data"""
        server_dir = get_server_dir(guild_id)
        return {
            'snapshots': server_dir / "member_snapshots.json",
            'config': server_dir / "analytics_config.json"
        }
        
    def get_timezone():
        """Get the configured timezone or default to UTC"""
        return getConfigData().get(TIMEZONE_CONFIG_KEY, DEFAULT_TIMEZONE)
        
    def get_timezone_offset():
        """Get the timezone offset in hours from UTC"""
        timezone = get_timezone()
        return TIMEZONE_OFFSETS.get(timezone, 0)
        
    def format_time_in_timezone(utc_time, format_str="%b %d, %I:%M %p"):
        """Format a UTC time in the configured timezone"""
        timezone = get_timezone()
        offset = get_timezone_offset()
        
        # Apply the offset
        local_time = utc_time + timedelta(hours=offset)
        
        # Format the time
        formatted_time = local_time.strftime(format_str)
        
        # Add the timezone abbreviation
        return f"{formatted_time} {timezone}"
    
    # Server configuration management
    def load_server_config(guild_id):
        """Load server-specific configuration"""
        files = get_server_files(guild_id)
        
        # Create default config if it doesn't exist
        if not files['config'].exists():
            default_config = {
                "auto_snapshot": False,
                "last_auto_snapshot": None,
                "first_snapshot_date": None,
                "chart_style": "emoji",  # Options: emoji, text
                "snapshot_retention_days": DATA_RETENTION_DAYS,
                "auto_snapshot_interval_hours": DEFAULT_AUTO_SNAPSHOT_INTERVAL_HOURS,
            }
            save_data(files['config'], default_config)
            return default_config
            
        return load_data(files['config'])
        
    def update_server_config(guild_id, key, value):
        """Update a specific server configuration value"""
        files = get_server_files(guild_id)
        config = load_server_config(guild_id)
        config[key] = value
        save_data(files['config'], config)
        return config
        
    def is_auto_snapshot_enabled(guild_id):
        """Check if automatic snapshots are enabled for this server"""
        config = load_server_config(guild_id)
        return config.get("auto_snapshot", False)
        
    def should_take_auto_snapshot(guild_id):
        """Return True if enough time has passed for an automatic snapshot."""
        config = load_server_config(guild_id)
        last_snapshot = config.get("last_auto_snapshot")
        interval = config.get(
            "auto_snapshot_interval_hours",
            DEFAULT_AUTO_SNAPSHOT_INTERVAL_HOURS,
        )

        if not last_snapshot:
            return True

        last_time = datetime.fromisoformat(last_snapshot)
        now = datetime.utcnow()

        return (now - last_time).total_seconds() >= interval * 3600

    # Initialize data structures if they don't exist
    def initialize_data(guild_id):
        files = get_server_files(guild_id)
        
        if not files['snapshots'].exists():
            with open(files['snapshots'], "w") as f:
                json.dump({"snapshots": []}, f, indent=4)
        
        # Initialize server config
        load_server_config(guild_id)

    # Load data from JSON files
    def load_data(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # Save data to JSON files
    def save_data(file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    # Take a server snapshot
    async def take_snapshot(guild, is_auto=False):
        files = get_server_files(guild.id)
        initialize_data(guild.id)  # Ensure files exist
        
        # Load existing data
        data = load_data(files['snapshots'])
        
        # Get channel and role counts
        voice_channels = 0
        text_channels = 0
        categories = 0
        for channel in guild.channels:
            channel_type = str(channel.type).lower()
            if channel_type == "text":
                text_channels += 1
            elif channel_type == "voice":
                voice_channels += 1
            elif channel_type == "category":
                categories += 1
        
        # Create snapshot
        timestamp = datetime.utcnow()
        snapshot = {
            "timestamp": timestamp.isoformat(),
            "member_count": guild.member_count,
            "channel_count": len(guild.channels),
            "role_count": len(guild.roles),
            "categories": categories,
            "text_channels": text_channels,
            "voice_channels": voice_channels,
            "bots": len([m for m in guild.members if m.bot]),
            "is_auto": is_auto
        }
        
        if "snapshots" not in data:
            data["snapshots"] = []
            
        data["snapshots"].append(snapshot)
        
        # Update server config
        config = load_server_config(guild.id)
        if is_auto:
            config["last_auto_snapshot"] = timestamp.isoformat()
            
        # Store first snapshot date if this is the first one
        if not config.get("first_snapshot_date") and data["snapshots"]:
            config["first_snapshot_date"] = data["snapshots"][0]["timestamp"]
            
        save_data(files['config'], config)
        
        # Remove old snapshots
        retention_days = config.get("snapshot_retention_days", DATA_RETENTION_DAYS)
        cutoff = (datetime.utcnow() - timedelta(days=retention_days)).isoformat()
        data["snapshots"] = [s for s in data["snapshots"] if s["timestamp"] > cutoff]
        
        save_data(files['snapshots'], data)
        return snapshot

    # Handle auto-snapshot functionality
    @bot.listen("on_message")
    async def auto_snapshot_handler(message):
        # Only trigger on chance to prevent excessive checks
        if random.random() > 0.05:  # Only run 5% of the time
            return
            
        # Skip if this is a DM or not in a guild
        if not message.guild:
            return
            
        # Check if auto-snapshots are enabled for this guild
        if not is_auto_snapshot_enabled(message.guild.id):
            return
            
        # Check if enough time has passed since last auto snapshot
        if not should_take_auto_snapshot(message.guild.id):
            return
            
        # Take the snapshot silently
        try:
            await take_snapshot(message.guild, is_auto=True)
            print(f"Auto-snapshot taken for {message.guild.name} (ID: {message.guild.id})", type_="INFO")
        except Exception as e:
            print(f"Error taking auto-snapshot: {str(e)}", type_="ERROR")
            
    # Analyze member growth trends
    def analyze_growth_trend(snapshots, days=7):
        """Analyze member growth trends and predict future growth"""
        if len(snapshots) < 2:
            return {
                "trend": "insufficient_data",
                "growth_rate_daily": 0,
                "prediction_7_days": None,
                "prediction_30_days": None,
                "confidence": "low"
            }
            
        # Sort snapshots by timestamp
        sorted_snapshots = sorted(snapshots, key=lambda x: x["timestamp"])
        
        # Get the most recent snapshot
        current = sorted_snapshots[-1]
        current_time = datetime.fromisoformat(current["timestamp"])
        current_count = current["member_count"]
        
        # Find a snapshot from approximately 'days' days ago
        target_time = current_time - timedelta(days=days)
        closest_snapshot = min(sorted_snapshots[:-1], 
                              key=lambda x: abs(datetime.fromisoformat(x["timestamp"]) - target_time))
        past_time = datetime.fromisoformat(closest_snapshot["timestamp"])
        past_count = closest_snapshot["member_count"]
        
        # Calculate time difference in days
        time_diff_days = (current_time - past_time).total_seconds() / (24 * 3600)
        
        # If time difference is too small, adjust analysis
        if time_diff_days < 1:
            time_diff_days = 1  # Minimum 1 day to avoid division issues
            
        # Calculate growth
        member_diff = current_count - past_count
        growth_rate_daily = member_diff / time_diff_days
        
        # Determine trend type
        if member_diff > 0:
            if growth_rate_daily >= 10:
                trend = "rapid_growth"
            elif growth_rate_daily >= 3:
                trend = "steady_growth"
            else:
                trend = "slow_growth"
        elif member_diff < 0:
            if growth_rate_daily <= -10:
                trend = "rapid_decline"
            elif growth_rate_daily <= -3:
                trend = "steady_decline"
            else:
                trend = "slow_decline"
        else:
            trend = "stable"
            
        # Make predictions
        prediction_7_days = round(current_count + (growth_rate_daily * 7))
        prediction_30_days = round(current_count + (growth_rate_daily * 30))
        
        # Determine confidence based on data points and consistency
        # More snapshots and consistent growth pattern = higher confidence
        if len(snapshots) >= 10:
            confidence = "high"
        elif len(snapshots) >= 5:
            confidence = "medium"
        else:
            confidence = "low"
            
        return {
            "trend": trend,
            "growth_rate_daily": growth_rate_daily,
            "growth_total": member_diff,
            "days_measured": round(time_diff_days, 1),
            "prediction_7_days": prediction_7_days,
            "prediction_30_days": prediction_30_days,
            "confidence": confidence
        }

    # Commands
    @bot.command(name="analytics", description="Server analytics commands")
    async def analytics_cmd(ctx, *, args: str = ""):
        # Store message for later deletion
        cmd_msg = ctx.message
        
        try:
            await cmd_msg.delete()
        except Exception as e:
            print(f"Error deleting command message: {str(e)}", type_="WARNING")
        
        args = args.strip().lower()
        
        # Parse arguments
        parts = args.split()
        cmd = parts[0] if parts else ""
        subcmd = parts[1] if len(parts) > 1 else ""
        
        if cmd == "snapshot":
            snapshot = await take_snapshot(ctx.guild)
            await ctx.send(f""" **New Snapshot**
            
**Server**: {ctx.guild.name}
**Members**: {snapshot["member_count"]:,}
**Channels**: {snapshot["channel_count"]:,}
**Time**: {format_time_in_timezone(datetime.fromisoformat(snapshot["timestamp"]), "%H:%M:%S")}""")
        
        elif cmd == "report":
            await generate_report(ctx)
            
        elif cmd == "clear":
            initialize_data(ctx.guild.id)
            await ctx.send(f"analytics data for {ctx.guild.name} has been cleared.")
            
        elif cmd == "status":
            await show_status(ctx)
            
        elif cmd == "members":
            await generate_member_graph(ctx)
            
        elif cmd == "trend":
            await show_trend_analysis(ctx)
            
        elif cmd == "compare":
            # Default to 7 days if not specified
            days = 7
            if subcmd and subcmd.isdigit():
                days = int(subcmd)
            await compare_periods(ctx, days)
            
        elif cmd == "export":
            await export_data(ctx)

        elif cmd == "auto":
            if subcmd in ["on", "true", "yes", "enable", "1"]:
                update_server_config(ctx.guild.id, "auto_snapshot", True)
                await ctx.send("automatic daily snapshots enabled")
            elif subcmd in ["off", "false", "no", "disable", "0"]:
                update_server_config(ctx.guild.id, "auto_snapshot", False)
                await ctx.send("automatic daily snapshots disabled")
            else:
                is_enabled = is_auto_snapshot_enabled(ctx.guild.id)
                status = "enabled" if is_enabled else "disabled"
                await ctx.send(f""" **auto-snapshot status**
                
automatic daily snapshots are currently {status}.

use `<p>analytics auto on` to enable
use `<p>analytics auto off` to disable""")

        elif cmd == "retention":
            if subcmd.isdigit():
                days = int(subcmd)
                update_server_config(ctx.guild.id, "snapshot_retention_days", days)
                await ctx.send(f"data retention set to {days} days")
            else:
                current = load_server_config(ctx.guild.id).get(
                    "snapshot_retention_days", DATA_RETENTION_DAYS
                )
                await ctx.send(f"data retention is {current} days")

        elif cmd == "interval":
            if subcmd:
                try:
                    hours = float(subcmd)
                    update_server_config(
                        ctx.guild.id, "auto_snapshot_interval_hours", hours
                    )
                    await ctx.send(
                        f"automatic snapshot interval set to {hours} hours"
                    )
                except ValueError:
                    await ctx.send("invalid subcommand. use `<p>analytics help` for a list of commands.")
            else:
                current = load_server_config(ctx.guild.id).get(
                    "auto_snapshot_interval_hours",
                    DEFAULT_AUTO_SNAPSHOT_INTERVAL_HOURS,
                )
                await ctx.send(
                    f"automatic snapshot interval is {current} hours"
                )
            
        else:
            await ctx.send(""" **server analytics commands**

• `<p>analytics snapshot` - take a snapshot
• `<p>analytics report` - generate detailed report
• `<p>analytics clear` - clear data
• `<p>analytics status` - show collection status
• `<p>analytics members` - show recent member changes
• `<p>analytics trend` - show growth trend analysis
• `<p>analytics compare [days]` - compare with previous period
• `<p>analytics export` - export data to text file
• `<p>analytics auto [on/off]` - manage automatic snapshots
• `<p>analytics retention [days]` - set data retention period
• `<p>analytics interval [hours]` - set auto snapshot interval
• `<p>a <subcommand>` - shorthand for commands
• `<p>a ss` - quick snapshot
• `<p>a timezone <zone>` - set timezone""")

    # Short command alternative
    @bot.command(name="a", description="short command for server analytics")
    async def short_analytics_cmd(ctx, *, args: str = ""):
        # Store message for later deletion
        cmd_msg = ctx.message
        
        try:
            await cmd_msg.delete()
        except Exception as e:
            print(f"error deleting command message: {str(e)}", type_="warning")
        
        args = args.strip().lower()
        parts = args.split()
        cmd = parts[0] if parts else ""
        
        # Handle the "ss" shorthand for snapshot
        if cmd == "ss":
            snapshot = await take_snapshot(ctx.guild)
            await ctx.send(f""" **new snapshot**
            
**server**: {ctx.guild.name}
**members**: {snapshot["member_count"]:,}
**channels**: {snapshot["channel_count"]:,}
**time**: {format_time_in_timezone(datetime.fromisoformat(snapshot["timestamp"]), "%h:%m:%s")}""")
            return
            
        # Handle timezone setting
        if cmd == "timezone":
            timezone = " ".join(parts[1:]).strip().upper() if len(parts) > 1 else ""
            
            if not timezone:
                current_tz = get_timezone()
                await ctx.send(f"current timezone is set to **{current_tz}**")
                return
                
            # Validate timezone
            if timezone in TIMEZONE_OFFSETS:
                updateConfigData(TIMEZONE_CONFIG_KEY, timezone)
                await ctx.send(f"timezone set to **{timezone}**")
            else:
                # Show available timezones
                timezone_list = ", ".join(sorted(TIMEZONE_OFFSETS.keys()))
                await ctx.send(f""" invalid timezone: **{timezone}**

available timezones:
{timezone_list}

usage: `<p>a timezone <zone>`""")
            return
            
        # Reuse the same logic as the analytics command for other subcommands
        await analytics_cmd(ctx, args=args)

    # Show analytics status
    async def show_status(ctx):
        files = get_server_files(ctx.guild.id)
        data = load_data(files['snapshots'])
        snapshots = data.get("snapshots", [])
        config = load_server_config(ctx.guild.id)
        
        # Save current private setting and update it
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            if not snapshots:
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content="no analytics data available yet for this server.",
                    title=f"analytics status: {ctx.guild.name}",
                    image=None
                )
            else:
                latest = snapshots[-1]
                latest_time = format_time_in_timezone(datetime.fromisoformat(latest["timestamp"]), "%y-%m-%d %h:%m")
                
                # Count auto snapshots
                auto_count = len([s for s in snapshots if s.get("is_auto", False)])
                manual_count = len(snapshots) - auto_count
                
                # Auto snapshot status
                auto_status = "enabled" if config.get("auto_snapshot", False) else "disabled"
                
                # Calculate average daily snapshots
                if len(snapshots) >= 2:
                    first_snapshot = min(snapshots, key=lambda x: x["timestamp"])
                    first_time = datetime.fromisoformat(first_snapshot["timestamp"])
                    time_span = (datetime.utcnow() - first_time).total_seconds() / (24 * 3600)
                    if time_span > 0:
                        avg_daily = len(snapshots) / time_span
                    else:
                        avg_daily = len(snapshots)
                else:
                    avg_daily = len(snapshots)
                
                status_content = f"""**total snapshots**: {len(snapshots):,} ({manual_count:,} manual, {auto_count:,} automatic)
**last update**: {latest_time}
**members tracked**: {latest["member_count"]:,}
**auto-snapshots**: {auto_status}
**average**: {avg_daily:.1f} snapshots per day

*data is retained for {config.get("snapshot_retention_days", DATA_RETENTION_DAYS)} days*"""
                
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content=status_content,
                    title=f"analytics status: {ctx.guild.name}",
                    image=None
                )
        finally:
            # Always restore private setting
            updateConfigData("private", current_private)

    # Generate analytics report
    async def generate_report(ctx):
        files = get_server_files(ctx.guild.id)
        initialize_data(ctx.guild.id)  # Ensure files exist
        
        data = load_data(files['snapshots'])
        snapshots = data.get("snapshots", [])
        
        if not snapshots:
            # Save current private setting and update it
            current_private = getConfigData().get("private")
            updateConfigData("private", False)
            
            try:
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content="no analytics data available yet for this server.",
                    title="server analytics report",
                    image=None
                )
            finally:
                # Always restore private setting
                updateConfigData("private", current_private)
            return
            
        # Calculate basic statistics
        latest = snapshots[-1]
        oldest = snapshots[0]
        growth = latest["member_count"] - oldest["member_count"]
        growth_rate = (growth / oldest["member_count"]) * 100 if oldest["member_count"] > 0 else 0
        
        # Find peak member count in the dataset
        peak_members = max(s["member_count"] for s in snapshots)
        current_members = latest["member_count"]
        members_from_peak = current_members - peak_members
        
        # Get trend analysis
        trend_data = analyze_growth_trend(snapshots)
        
        # Format growth rate for display
        daily_change = trend_data["growth_rate_daily"]
        if daily_change >= 0:
            daily_growth_display = f"+{daily_change:.1f}"
        else:
            daily_growth_display = f"{daily_change:.1f}"
        
        # Calculate membership milestone
        next_milestone = 0
        if current_members < 100:
            next_milestone = 100
        elif current_members < 500:
            next_milestone = 500
        elif current_members < 1000:
            next_milestone = 1000
        else:
            # Next 1000 milestone
            next_milestone = math.ceil(current_members / 1000) * 1000
            
        days_to_milestone = "∞"
        if daily_change > 0:
            days_to_milestone = math.ceil((next_milestone - current_members) / daily_change)
            
        # Save current private setting and update it
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            # Generate report
            report = f"""## server overview
            
**member statistics**
• total members: **{current_members:,}**
• peak members: **{peak_members:,}**
• members from peak: **{members_from_peak:+,}** members
• bots: **{latest.get("bots", 0):,}**
• human users: **{latest["member_count"] - latest.get("bots", 0):,}**

**channel information**
• total channels: **{latest["channel_count"]:,}**
• text channels: **{latest.get("text_channels", 0):,}**
• voice channels: **{latest.get("voice_channels", 0):,}**
• categories: **{latest.get("categories", 0):,}**

**role count**
• total roles: **{latest["role_count"]:,}**

**growth analysis**
• current trend: **{trend_data["trend"].replace("_", " ").title()}**
• daily change: **{daily_growth_display}** members/day
• member growth: **{growth:+,}** members total
• growth rate: **{growth_rate:,.2f}%**
• next milestone: **{next_milestone:,}** members
• est. days to milestone: **{days_to_milestone}** days

*last updated: {format_time_in_timezone(datetime.fromisoformat(latest["timestamp"]), "%y-%m-%d %h:%m")}*
server analytics
"""
            
            # Send the embed
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=report,
                title=f"server analytics report: {ctx.guild.name}",
                image=None
            )
                
        except Exception as e:
            print(f"error generating report: {str(e)}", type_="error")
            await ctx.send(f"error generating analytics report for {ctx.guild.name}. please try again later.")
        finally:
            # Always restore private setting
            updateConfigData("private", current_private)
            
    # Show trend analysis
    async def show_trend_analysis(ctx):
        files = get_server_files(ctx.guild.id)
        data = load_data(files['snapshots'])
        snapshots = data.get("snapshots", [])
        
        # Save current private setting and update it
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            if len(snapshots) < 2:
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content="not enough data for trend analysis. please take at least 2 snapshots.",
                    title=f"growth trend analysis: {ctx.guild.name}",
                    image=None
                )
                return
                
            # Get trend analysis for different time periods
            short_trend = analyze_growth_trend(snapshots, days=3)
            medium_trend = analyze_growth_trend(snapshots, days=7)
            long_trend = analyze_growth_trend(snapshots, days=14)
            
            # Format the trend analysis
            latest = max(snapshots, key=lambda x: x["timestamp"])
            current_members = latest["member_count"]
            
            trend_content = f"""## member growth analysis

**current members:** {current_members:,}

**short-term trend:** {short_trend["trend"].replace("_", " ").title()}
• daily change: **{short_trend["growth_rate_daily"]:.1f}** members/day
• 7-day projection: **{short_trend["prediction_7_days"]:,}** members
• confidence: {short_trend["confidence"].title()}

**medium-term trend:** {medium_trend["trend"].replace("_", " ").title()}
• daily change: **{medium_trend["growth_rate_daily"]:.1f}** members/day
• 30-day projection: **{medium_trend["prediction_30_days"]:,}** members
• confidence: {medium_trend["confidence"].title()}

**long-term trend:** {long_trend["trend"].replace("_", " ").title()}
• over {long_trend["days_measured"]} days
• total change: **{long_trend["growth_total"]:+,}** members

*note: projections are estimates based on current trends*
*last updated: {format_time_in_timezone(datetime.fromisoformat(latest["timestamp"]), "%y-%m-%d %h:%m")}*
"""
            
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=trend_content,
                title=f"growth trend analysis: {ctx.guild.name}",
                image=None
            )
        except Exception as e:
            print(f"error generating trend analysis: {str(e)}", type_="error")
            await ctx.send(f"error generating trend analysis for {ctx.guild.name}. please try again later.")
        finally:
            # Always restore private setting
            updateConfigData("private", current_private)
            
    # Compare server stats between time periods
    async def compare_periods(ctx, days=7):
        files = get_server_files(ctx.guild.id)
        data = load_data(files['snapshots'])
        snapshots = data.get("snapshots", [])
        
        # Save current private setting and update it
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            if len(snapshots) < 2:
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content="not enough data for comparison. please take at least 2 snapshots.",
                    title=f"comparison report: last {days} days - {ctx.guild.name}",
                    image=None
                )
                return
                
            # Sort snapshots by timestamp
            sorted_snapshots = sorted(snapshots, key=lambda x: x["timestamp"])
            
            # Get the most recent snapshot
            current = sorted_snapshots[-1]
            current_time = datetime.fromisoformat(current["timestamp"])
            
            # Find a snapshot from approximately 'days' days ago
            target_time = current_time - timedelta(days=days)
            previous = min(sorted_snapshots[:-1], 
                           key=lambda x: abs(datetime.fromisoformat(x["timestamp"]) - target_time))
            previous_time = datetime.fromisoformat(previous["timestamp"])
            
            # Calculate actual days between snapshots
            days_diff = (current_time - previous_time).total_seconds() / (24 * 3600)
            
            # Calculate differences
            member_diff = current["member_count"] - previous["member_count"]
            member_percent = (member_diff / previous["member_count"]) * 100 if previous["member_count"] > 0 else 0
            
            channel_diff = current["channel_count"] - previous["channel_count"]
            role_diff = current["role_count"] - previous["role_count"]
            
            # Format dates
            current_date = format_time_in_timezone(current_time, "%y-%m-%d %h:%m")
            previous_date = format_time_in_timezone(previous_time, "%y-%m-%d %h:%m")
            
            # Build comparison message
            comparison = f"""## server comparison

**time period:** {days_diff:.1f} days
**from:** {previous_date}
**to:** {current_date}

**member changes**
• before: **{previous["member_count"]:,}** members
• now: **{current["member_count"]:,}** members
• change: **{member_diff:+,}** members ({member_percent:+.2f}%)
• bots: **{current.get("bots", 0) - previous.get("bots", 0):+,}**

**channel changes**
• total: **{channel_diff:+,}** channels
• text: **{current.get("text_channels", 0) - previous.get("text_channels", 0):+,}**
• voice: **{current.get("voice_channels", 0) - previous.get("voice_channels", 0):+,}**

**role changes**
• total: **{role_diff:+,}** roles

*server comparison between two points in time*
"""
            
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=comparison,
                title=f"comparison report: last {days} days - {ctx.guild.name}",
                image=None
            )
        except Exception as e:
            print(f"error generating comparison: {str(e)}", type_="error")
            await ctx.send(f"error generating server comparison for {ctx.guild.name}. please try again later.")
        finally:
            # Always restore private setting
            updateConfigData("private", current_private)
            
    # Export analytics data to text file
    async def export_data(ctx):
        files = get_server_files(ctx.guild.id)
        data = load_data(files['snapshots'])
        snapshots = data.get("snapshots", [])
        
        if not snapshots:
            await ctx.send("no analytics data available to export.")
            return
            
        try:
            # Sort snapshots chronologically
            sorted_snapshots = sorted(snapshots, key=lambda x: x["timestamp"])
            
            # Create a formatted text file
            export_text = f"# server analytics export - {ctx.guild.name}\n"
            export_text += f"# generated on {datetime.utcnow().strftime('%y-%m-%d %h:%m:%s')} utc\n"
            export_text += f"# total snapshots: {len(snapshots)}\n\n"
            
            export_text += "timestamp,member_count,channel_count,text_channels,voice_channels,categories,role_count,bots\n"
            
            for snapshot in sorted_snapshots:
                timestamp = snapshot["timestamp"]
                member_count = snapshot["member_count"]
                channel_count = snapshot["channel_count"]
                text_channels = snapshot.get("text_channels", 0)
                voice_channels = snapshot.get("voice_channels", 0)
                categories = snapshot.get("categories", 0)
                role_count = snapshot["role_count"]
                bots = snapshot.get("bots", 0)
                
                export_text += f"{timestamp},{member_count},{channel_count},{text_channels},{voice_channels},{categories},{role_count},{bots}\n"
                
            # Create a temporary file in the exports directory
            export_dir = Path(getScriptsPath()) / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{ctx.guild.id}_analytics_{datetime.utcnow().strftime('%y%m%d_%h%m%S')}.csv"
            export_path = export_dir / filename
            
            with open(export_path, "w") as f:
                f.write(export_text)
                
            await ctx.send(f""" **analytics data export complete**

**file:** `{filename}`
**location:** `{export_path}`
**snapshots:** {len(snapshots)}
**format:** csv (comma-separated values)

*use your file manager to access the exported data*""")
            
        except Exception as e:
            print(f"error exporting data: {str(e)}", type_="error")
            await ctx.send(f"error exporting analytics data. please try again later.")

    # Generate member change graph
    async def generate_member_graph(ctx):
        files = get_server_files(ctx.guild.id)
        initialize_data(ctx.guild.id)  # Ensure files exist
        
        data = load_data(files['snapshots'])
        snapshots = data.get("snapshots", [])
        
        # Save current private setting and update it
        current_private = getConfigData().get("private")
        updateConfigData("private", False)
        
        try:
            if not snapshots:
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content="no analytics data available yet for this server.",
                    title=f"member count history: {ctx.guild.name}",
                    image=None
                )
                return
            
            # Sort snapshots by timestamp (newest first)
            snapshots.sort(key=lambda x: datetime.fromisoformat(x["timestamp"]), reverse=True)
            
            # Take only the 7 most recent snapshots (more than before)
            recent_snapshots = snapshots[:7]
            
            # Group snapshots with the same member count
            grouped_snapshots = []
            current_group = []
            
            for snapshot in recent_snapshots:
                if not current_group:
                    current_group.append(snapshot)
                elif snapshot["member_count"] == current_group[0]["member_count"]:
                    current_group.append(snapshot)
                else:
                    if current_group:
                        grouped_snapshots.append(current_group)
                    current_group = [snapshot]
            
            if current_group:
                grouped_snapshots.append(current_group)
            
            # Create the graph content
            graph_content = ""
            
            # Add overall member count and trend
            if grouped_snapshots:
                current_members = grouped_snapshots[0][0]["member_count"]
                
                # Get overall change if enough snapshots
                if len(grouped_snapshots) >= 2:
                    first_members = grouped_snapshots[-1][0]["member_count"]
                    overall_change = current_members - first_members
                    
                    graph_content += f"**current members:** {current_members:,} ({overall_change:+,})\n\n"
                else:
                    graph_content += f"**current members:** {current_members:,}\n\n"
            
            # Process each group and calculate changes
            for i, group in enumerate(grouped_snapshots):
                snapshot = group[0]  # Use most recent snapshot in group
                current_count = snapshot["member_count"]
                
                # Convert UTC to configured timezone
                utc_time = datetime.fromisoformat(snapshot["timestamp"])
                time_str = format_time_in_timezone(utc_time)
                
                # Calculate member change and trend indicator
                change_str = ""
                trend = ""
                
                # Compare with the next snapshot if available
                if i < len(grouped_snapshots) - 1:
                    next_snapshot = grouped_snapshots[i + 1][0]
                    change = current_count - next_snapshot["member_count"]
                    if change > 0:
                        change_str = f" (+{change})"
                    elif change < 0:
                        change_str = f" ({change})"
                
                # Create the line with more detail
                if len(group) > 1:
                    earliest = datetime.fromisoformat(group[-1]["timestamp"])
                    earliest_time = format_time_in_timezone(earliest, "%i:%m %p")
                    current_time = format_time_in_timezone(utc_time, "%i:%m %p")
                    date_str = format_time_in_timezone(utc_time, "%b %d")
                    duration = (utc_time - earliest).total_seconds() / 3600  # hours
                    
                    # Swap the order to show earlier time first
                    graph_content += f"**{date_str}:** **{earliest_time}** → **{current_time}** ({duration:.1f}h)\n"
                    graph_content += f"Members: **{current_count:,}**{change_str}{trend}\n\n"
                else:
                    is_auto = snapshot.get("is_auto", False)
                    source = " (auto)" if is_auto else ""
                    graph_content += f"**{time_str}**{source}\n"
                    graph_content += f"Members: **{current_count:,}**{change_str}{trend}\n\n"
            
            # Send the graph as an embed
            await forwardEmbedMethod(
                channel_id=ctx.channel.id,
                content=graph_content,
                title=f"member count history - {ctx.guild.name}",
                image=None
            )
        except Exception as e:
            print(f"Error generating member graph: {str(e)}", type_="ERROR")
            await ctx.send(f"error generating member graph for {ctx.guild.name}. please try again later.")
        finally:
            # Always restore private setting
            updateConfigData("private", current_private)

server_analytics()  # Initialize the script 
