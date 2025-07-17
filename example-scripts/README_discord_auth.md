# Discord Auth Bot (NightyScript + SQLite3)

This bot provides a simple verification system for Discord servers using NightyScript and SQLite3.

## Features
- Creates a `verification` channel only visible to users with the `Unverified` role and admins.
- Users verify by sending `!verify <key>` in the channel.
- Admins can generate keys with `!genkey`.
- Keys are tracked in a local SQLite3 database.

## Setup
1. **Install dependencies:**
   - `pip install discord.py sqlite3`
2. **Configure the bot:**
   - Edit `example-scripts/discord_auth.nighty`:
     - Replace `YOUR_BOT_TOKEN_HERE` with your bot token.
     - Replace `GUILD_ID` with your server's ID.
3. **Run the bot:**
   - `python3 example-scripts/discord_auth.nighty`

## Usage
- Users with the `Unverified` role (or no roles) will see the `#verification` channel.
- Admins can generate a key with `!genkey` in the channel.
- Users verify by sending `!verify <key>`.
- On success, the user is given the `Verified` role and removed from `Unverified`.

## Notes
- The bot will auto-create the `Verified` and `Unverified` roles if they do not exist.
- The SQLite3 database (`discord_auth.sqlite3`) is created in the working directory.
- Only admins can use `!genkey`.