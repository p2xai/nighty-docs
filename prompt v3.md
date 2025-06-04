# NightyScript Documentation v4.4 (Public)

**Created by:** thedorekaczynski

**Made with:** [manus.im](https://manus.im) and [claude.ai](https://claude.ai)

---

## 1. Overview

NightyScript extends Nighty (a Discord selfbot) with custom Python scripts. Scripts define commands and event handlers. Nighty manages the Discord connection; scripts focus purely on functionality. It is built on a modified version of the discord.py-self library.

**Do not** use standard `discord.py` libraries directly, except as documented.

### 1.1 Prohibited Imports

The following imports will cause script failure:

```python
import discord
import nighty
from discord import *
from nighty import *
from nighty import bot, nightyScript, getScriptsPath, Tab, UI
import matplotlib  # or any matplotlib-related imports
```

* Any other imports from `discord.py` or `nighty` packages.

You may use objects like `discord.File` without importing them — NightyScript makes them available via its built-in API.

### 1.2 Guidelines 

* Only use standard Python imports and NightyScript-provided functions.
* External Python packages (e.g. `pydub`, `numpy`, `matplotlib`) are not allowed, unless they are non-Python tools like Docker.
* All dependencies must be documented inside the script's docstring.

### 1.3 Embed Limitation

`discord.Embed` is not supported. Use `forwardEmbedMethod` to send embed-style messages in NightyScript.

### 1.4 Discord API Limitations

NightyScript cannot:

* Cache users globally.
* Access complete server member lists.
* Scan all servers to build a user map.

These limitations are enforced by Discord's API. Scripts should operate only within the context of users interacting in channels the selfbot can access.

---

## 2. Script Structure

Create scripts using the `@nightyScript` decorator:

```python
@nightyScript(
    name="Script Name",
    author="Your Name",
    description="Description",
    usage="<p>command <args>"
)
def script_function():
    # Script logic
    pass

script_function()  # IMPORTANT: Call to initialize
```

**name**: Script's display name (string).

**author**: Script creator (string). Use your name or alias.

**description**: Brief explanation (string).

**usage**: Command syntax. `<p>` is the user's configured prefix. `[]` denotes optional arguments, `--` indicates flags (string).

The decorated function (`script_function`) is the script's entry point. It's called on script load.

`script_function()` (Call): Must be called at the end of the script to register commands and listeners with Nighty.

### 2.1 Documentation Standards

Scripts should include comprehensive documentation following these standards:

#### 2.1.1 Script-Level Documentation
Add a docstring at the start of your main script function:

```python
def script_function():
    """
    SCRIPT NAME
    ----------

    Brief description of what the script does and its main purpose.

    COMMANDS:
    <p>command1 <args> - Description of command1
    <p>command2 [args] - Description of command2

    EXAMPLES:
    <p>command1 arg1 arg2 - Example usage of command1
    <p>command2 --flag     - Example usage of command2 with flags

    NOTES:
    - Important note about functionality
    - Any setup requirements (like external tools, API keys)
    - Special considerations or limitations
    """
    # ... script logic ...
```

#### 2.1.2 Command Documentation
Each command should have a clear description in its decorator:

```python
@bot.command(
    name="command",
    description="Clear, concise description of what the command does"
)
```

#### 2.1.3 Code Comments
- Use comments to explain complex logic or non-obvious code
- Keep comments concise but informative
- Use inline comments sparingly and only when necessary
- Document any important assumptions or edge cases

#### 2.1.4 Best Practices
1.  **Consistency**: Follow the same documentation format across all scripts
2.  **Clarity**: Use clear, simple language
3.  **Completeness**: Document all commands, arguments, and flags
4.  **Examples**: Include practical examples for each command
5.  **Notes**: Highlight any important setup requirements or limitations
6.  **Updates**: Keep documentation in sync with code changes
7.  **Self-Contained**: Include all documentation and requirements within the script itself

## 3. Command Prefix

`<p>` in usage strings represents the user's configured command prefix. Scripts do not handle prefix detection directly.

## 4. Core Functions

### 4.1 Configuration (getConfigData, updateConfigData)

NightyScript provides a key-value store for configuration:

Get a configuration value, providing a default if it's not set:
```python
value = getConfigData().get("my_key", "default_value")
```

Set or update a configuration value:
```python
updateConfigData("my_key", "new_value")
```

**`getConfigData()`**: Returns the entire configuration dictionary. For accessing individual values, use the `.get(key, default)` method.

**`updateConfigData(key, value)`**: Sets or updates a configuration value.

**Best Practices**:

-   **Namespacing**: Use unique, descriptive keys (e.g., `scriptname_setting`) to avoid conflicts between scripts.
-   **Defaults**: Always use `.get(key, default)` to provide a default value if the key is not set.
-   **Error Handling**: Wrap configuration access in `try...except` blocks, especially during script initialization.
-   **Initialization**: Within your main script function, set default values for any configuration keys that might not be set by the user.

Note: Use JSON storage (see below) for lists of IDs or more complex data structures. The configuration system is best suited for simple key-value pairs like booleans, strings, or numbers.

### 4.2 JSON Storage

For persistent storage of complex data structures, use JSON files:

```python
from pathlib import Path
import json

BASE_DIR = Path(getScriptsPath()) / "json"  # Standard location
DATA_FILE = BASE_DIR / "my_script_data.json" # Use a script-specific name

BASE_DIR.mkdir(parents=True, exist_ok=True) # Ensure directory exists

# Initialize file if needed
if not DATA_FILE.exists():
    with open(DATA_FILE, "w") as f:
        json.dump({"default_key": []}, f, indent=4)

def load_data():
    """Loads data from the script's JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: {DATA_FILE} not found or invalid. Returning default.", type_="ERROR")
        return {"default_key": []} # Return default structure

def save_data(data):
    """Saves data to the script's JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data to {DATA_FILE}: {e}", type_="ERROR")

```

**Best Practices**:

-   **Directory**: Store JSON files in a `json/` subdirectory within the Nighty scripts directory. Use `getScriptsPath()` to ensure the correct location.
-   **Filename**: Use a unique, descriptive filename for your script's data (e.g., `my_script_data.json`).
-   **Initialization**: Check if the file exists, and create it with a default structure if it doesn't.
-   **Error Handling**: Use `try...except` blocks for all file operations (reading and writing) and log potential errors.
-   **Data Structure**: Design a clear and efficient JSON structure for your data.
-   **Helper Functions**: Use separate `load_data()` and `save_data()` functions to encapsulate file I/O.

### 4.3 Bot Commands (@bot.command)

Define commands using the `@bot.command` decorator:

```python
@bot.command(
    name="command",
    aliases=["c", "cmd"], # Optional list of aliases
    usage="<arg1> [--flag]",
    description="Desc"
)
async def command_handler(ctx, *, args: str):
    await ctx.message.delete() # Standard first step

    # Argument parsing example:
    parts = args.split()
    arg1 = parts[0] if parts else ""
    flag_present = "--flag" in parts

    if flag_present:
        # ... process flag ...
        pass

    # ... process arg1 ...

    msg = await ctx.send("Processing...")  # Optional status message
    # ... command logic ...
    await msg.delete()  # Delete the status message (if created)
```

**`name`**: The command name (string). This is how users will invoke the command.

**`aliases`**: Optional list of alternative command names (string array). Allows users to invoke the command using shorter or alternative names.

**`usage`**: A string describing the command's arguments and flags (for documentation).

**`description`**: A brief description of the command's purpose.

**`ctx`**: The command context (provided by Nighty). It contains information about the message that triggered the command (e.g., `ctx.message`, `ctx.channel`, `ctx.author`, `ctx.guild`).

**`args: str`**: All arguments passed to the command *after* the command name, as a single string. You are responsible for parsing this string.

**Best Practices**:

-   **`await ctx.message.delete()`**: Almost always delete the original command message to keep the chat clean and maintain privacy.
-   **Argument Parsing**: Use string methods (like `.split()`, `.strip()`, `.startswith()`, `.endswith()`, `.replace()`) or the `re` module (for regular expressions) to process the `args` string effectively. Consider using libraries like `argparse` within your handler if complexity warrants it, but remember no external packages can be *installed*.
-   **Status Messages**: For commands that take a noticeable amount of time, send a temporary status message (`await ctx.send("Processing...")`) and then delete it (`await msg.delete()`) or edit it (`await msg.edit(content="Done!")`) when the command is finished.
-   **Error Handling**: Use `try...except` blocks to catch potential errors during command execution (e.g., invalid input, API errors) and send user-friendly error messages to the chat (`await ctx.send("Error: Invalid input provided.")`).
-   **Aliases**: Use aliases to provide shorter or alternative command names, especially for frequently used commands. Keep aliases short and intuitive.

#### 4.3.1 Command Consolidation with Subcommands

For scripts with multiple related commands, consider consolidating them under a single main command with subcommands. This creates a more organized and intuitive interface.

##### Example Structure:

```python
@bot.command(
    name="maincommand",
    usage="<subcommand> [args] OR <default_action_arg> [--flags]",
    description="Main command with subcommands for various actions."
)
async def main_command(ctx, *, args: str):
    await ctx.message.delete()

    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    subargs = parts[1] if len(parts) > 1 else ""

    if subcommand == "add":
        await handle_add(ctx, args=subargs)
    elif subcommand == "remove":
        await handle_remove(ctx, args=subargs)
    elif subcommand == "list":
        await handle_list(ctx, args=subargs)
    elif subcommand == "config":
        await handle_config(ctx, args=subargs)
    elif subcommand in ["help", "?"] or not subcommand: # Handle help or empty input
        await show_main_help(ctx)
    else:
        # Default action if the first arg doesn't match a subcommand
        # Could treat 'args' as the input for the primary function
        # Example: Treat 'args' directly as a location for a weather command
        await handle_default_action(ctx, location=args)

# --- Helper functions for subcommands ---
async def handle_add(ctx, args):
    # ... logic to add something ...
    await ctx.send(f"Added: {args}")

async def handle_remove(ctx, args):
    # ... logic to remove something ...
    await ctx.send(f"Removed: {args}")

async def handle_list(ctx, args):
    # ... logic to list items ...
    await ctx.send("Listing items...")

async def handle_config(ctx, args):
    # ... logic to configure settings ...
    await ctx.send(f"Configuring: {args}")

async def handle_default_action(ctx, location):
    # ... logic for the main purpose (e.g., get weather for 'location') ...
    await ctx.send(f"Performing default action for: {location}")

async def show_main_help(ctx):
    """Shows help information for the main command and its subcommands."""
    help_text = f"""
**Command Help: `{getConfigData().get('prefix', '<p>')}maincommand`**

**Usage:**
`{getConfigData().get('prefix', '<p>')}maincommand <subcommand> [arguments]`
`{getConfigData().get('prefix', '<p>')}maincommand <default_action_argument>`

**Subcommands:**
- `add <item>`: Adds an item.
- `remove <item>`: Removes an item.
- `list`: Lists all items.
- `config <setting> <value>`: Configures a setting.
- `help` or `?`: Shows this help message.

**Default Action:**
If no subcommand is matched, performs the default action (e.g., fetching data for the provided argument).

**Examples:**
`{getConfigData().get('prefix', '<p>')}maincommand add MyItem`
`{getConfigData().get('prefix', '<p>')}maincommand list`
`{getConfigData().get('prefix', '<p>')}maincommand MyDefaultArg`
"""
    await ctx.send(help_text)

```

##### Benefits:

1.  **Organization**: Groups related functionality under one command.
2.  **Discoverability**: A single `help` subcommand can list all possibilities.
3.  **Reduced Clutter**: Fewer top-level commands.
4.  **Namespace**: Avoids potential conflicts with other scripts' command names.

##### Best Practices:

-   **Clear Subcommand Names**: Use intuitive verbs (add, remove, list, set, get, config) or nouns.
-   **Help Command**: Always include a `help` (or similar) subcommand.
-   **Default Action**: Decide if the command should have a primary function when no subcommand is given.
-   **Consistent Parsing**: Handle arguments (`subargs`) consistently across subcommands.
-   **Error Handling**: Provide clear messages for invalid subcommands or missing arguments.
-   **Documentation**: Update the main script docstring and the command's `usage`/`description` to reflect the subcommand structure.

#### 4.3.2 Sending Stickers

Discord allows bots to send both built-in and custom stickers. Use the `stickers` parameter of `ctx.send` and retrieve the sticker from the cache before falling back to an HTTP fetch. This avoids unnecessary network calls and speeds up repeat usage.

```python
STICKER_ID = 749054660769218631  # example ID for the "wave" sticker
sticker = bot.get_sticker(STICKER_ID)
if not sticker:
    sticker = await bot.fetch_sticker(STICKER_ID)
await ctx.send(stickers=[sticker])
```

`bot.get_sticker` returns `None` if the sticker is not cached. For custom stickers—those uploaded to a guild you have access to—you may need to fetch them the first time with `fetch_sticker`. Once fetched, they remain in the cache for subsequent calls to `get_sticker`.

#### 4.3.3 Sending Emojis

Custom guild emojis work similarly to stickers. Retrieve the emoji from the cache using `bot.get_emoji` and fall back to `bot.fetch_emoji` when necessary. Send the emoji by converting the object to a string.

```python
EMOJI_ID = 123456789012345678  # example custom emoji
emoji = bot.get_emoji(EMOJI_ID)
if not emoji:
    emoji = await bot.fetch_emoji(EMOJI_ID)
await ctx.send(str(emoji))
```

`get_emoji` returns `None` when the emoji isn't cached. After fetching once, the emoji remains cached for subsequent calls.

### 4.4 Event Listeners (@bot.listen)

Handle Discord events using the `@bot.listen` decorator:

```python
@bot.listen("on_message")
async def message_handler(message):
    # Ignore messages sent by the selfbot itself
    if message.author.id == bot.user.id:
        return

    # Ignore messages from other bots (optional, but often useful)
    if message.author.bot:
        return

    # Example: Auto-respond to a keyword
    if "hello there" in message.content.lower():
        try:
            await message.channel.send("General Kenobi!")
        except Exception as e:
            print(f"Error sending auto-response: {e}", type_="ERROR")

    # Example: Log edited messages (requires on_message_edit event)
@bot.listen("on_message_edit")
async def edit_logger(before, after):
     if after.author.id == bot.user.id: # Ignore self-edits
         return
     # Check if content actually changed
     if before.content != after.content:
         print(f"User {after.author} edited message in {after.channel}: '{before.content}' -> '{after.content}'", type_="INFO")

```

**`message`** (for `on_message`): The message object (provided by Nighty). Contains info like `message.content`, `message.author`, `message.channel`, `message.guild`.

**`before`, `after`** (for `on_message_edit`, `on_message_delete`, `on_voice_state_update`, etc.): Represent the state before and after the event. Consult discord.py documentation for specific event parameters, but remember you *cannot import `discord`*. NightyScript provides the necessary objects directly.

**Common Events**: `on_message`, `on_message_edit`, `on_message_delete`, `on_reaction_add`, `on_voice_state_update`. Check Nighty documentation or experiment to see which are fully supported.

**Best Practices**:

-   **Ignore Self**: *Always* include `if message.author.id == bot.user.id: return` (or similar check using the relevant object like `member.id` or `reaction.user_id`) to prevent loops and unintended actions on the selfbot's own messages/events.
-   **Ignore Bots**: Consider adding `if message.author.bot: return` if you don't want to react to other bots.
-   **Efficiency**: Event handlers run on *every* matching event. Keep the logic inside them as efficient as possible. Use filtering (see below) to avoid unnecessary processing.
-   **Permissions**: Ensure the selfbot has the necessary permissions in the channel/server for any actions the listener takes (e.g., `Send Messages`, `Read Message History`).
-   **Error Handling**: Wrap event handler logic in `try...except` blocks to prevent one faulty event from crashing the script. Log errors using `print(..., type_="ERROR")`.

### 4.5 Selective Event Handling (Filtering)

Limit event processing based on criteria like server ID, channel ID, or user ID. This is crucial for performance and targeted functionality. Use JSON storage (Section 4.2) for managing lists of IDs.

```python
# (Continuing the on_message example from 4.4)
import json
from pathlib import Path

# --- JSON Setup (similar to Section 4.2) ---
FILTER_BASE_DIR = Path(getScriptsPath()) / "json"
ALLOWED_SERVERS_FILE = FILTER_BASE_DIR / "autorespond_servers.json"
ALLOWED_USERS_FILE = FILTER_BASE_DIR / "autorespond_users.json"

def load_filtered_ids(file_path):
    # ... (use load_data logic from 4.2, returning empty list on error) ...
    FILTER_BASE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            # Ensure it returns a list of strings
            return [str(item) for item in data] if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# --- Event Listener with Filtering ---
@bot.listen("on_message")
async def filtered_message_handler(message):
    if message.author.id == bot.user.id or message.author.bot:
        return
    if not message.guild: # Ignore DMs for this example
        return

    # --- Filtering Logic ---
    allowed_servers = load_filtered_ids(ALLOWED_SERVERS_FILE)
    allowed_users = load_filtered_ids(ALLOWED_USERS_FILE)

    # If the allowed_servers list exists and is not empty,
    # check if the current server is in it.
    if allowed_servers and str(message.guild.id) not in allowed_servers:
        return # Ignore message if server not allowed

    # If the allowed_users list exists and is not empty,
    # check if the current author is in it.
    if allowed_users and str(message.author.id) not in allowed_users:
        return # Ignore message if user not allowed
    # --- End Filtering Logic ---

    # Proceed with functionality only if filters passed
    if "hello there" in message.content.lower():
        try:
            await message.channel.send("General Kenobi! (Filtered Response)")
        except Exception as e:
            print(f"Error sending filtered auto-response: {e}", type_="ERROR")

# --- Commands to Manage Filters (add these within your script_function) ---
# Example: Add server command
@bot.command(name="addrespondserver", description="Allow auto-responses in this server.")
async def add_respond_server(ctx, *, server_id: str):
    await ctx.message.delete()
    try:
        server_id = str(int(server_id)) # Basic validation
        servers = load_filtered_ids(ALLOWED_SERVERS_FILE)
        if server_id not in servers:
            servers.append(server_id)
            save_ids(ALLOWED_SERVERS_FILE, servers) # Use your save_data function
            await ctx.send(f"Server {server_id} added to auto-respond list.")
        else:
            await ctx.send("Server already in list.")
    except ValueError:
        await ctx.send("Invalid Server ID.")
    except Exception as e:
        await ctx.send(f"Error adding server: {e}")

# (Similarly, add commands for remove-server, list-servers, add-user, remove-user, list-users)

```

**Key Filtering Steps:**

1.  **Load Allowed IDs**: Read server/user IDs from your JSON files at the start of the listener.
2.  **Check Guild/Author**: Get the `message.guild.id` and `message.author.id` (or equivalent for other events). Convert them to strings for reliable comparison with JSON data.
3.  **Conditional Return**:
    *   Check if the allowed list exists (`allowed_servers` is not empty).
    *   If it exists, check if the current ID (`str(message.guild.id)`) is *not* in the list.
    *   If both conditions are true, `return` early to stop processing the event.
    *   Repeat for other criteria (users, channels).
4.  **Empty List Means All**: If an allowed list is empty (or doesn't exist), the filter for that criteria is effectively disabled (meaning all servers/users are allowed by that specific filter).

**Strongly Recommended**: Use JSON files for potentially large lists of IDs. The configuration system (`getConfigData`) is less suitable for this. Provide commands (`<p>addserver`, `<p>removeserver`, etc.) for users to manage these lists easily.

### 4.6 Message Sending

NightyScript provides several ways to send messages:

#### 4.6.1 Basic Text Messages

**`ctx.send(content)`**:
   - Sends a simple text message to the channel where a command was invoked.
   - Primarily used within `@bot.command` handlers.
   - Example: `await ctx.send("Command received!")`

**`message.channel.send(content)`**:
   - Sends a simple text message to the channel where a message event originated.
   - Primarily used within `@bot.listen("on_message")` handlers.
   - Example: `await message.channel.send("Keyword detected!")`

#### 4.6.2 Rich Embed Messages

**`forwardEmbedMethod(...)`**:
   - **The only way to send rich embed messages.** Do *not* attempt to use `discord.Embed`.
   - Sends an embed to a *specific* channel ID.
   - Requires keyword arguments.
   - **WARNING:** Only supports a limited set of parameters. Using unsupported parameters will raise errors like "unexpected keyword argument".

   ```python
   # Example within a command context
   await forwardEmbedMethod(
       channel_id=ctx.channel.id, # Target the command's channel (REQUIRED)
       content="# Important Announcement\n\n**Bold text** and *italic text*\n\n> Important note here\n\n- Bullet point 1\n- Bullet point 2\n  - Nested bullet\n\n1. Numbered item\n2. Second item\n\n[Link to documentation](https://example.com)", # Text with markdown formatting
       title="Message Title", # Optional title for the embed
       image="https://example.com/image.png" # Optional URL of an image to display
   )

   # Example within an event listener (sending to a specific log channel)
   log_channel_id = "123456789012345678" # Get from config or JSON
   await forwardEmbedMethod(
       channel_id=log_channel_id,
       content=f"# Event Detected\n\n**User:** {message.author}\n**Time:** {message.created_at}\n\n> Message content: {message.content}"
   )
   ```

   **`forwardEmbedMethod` Supported Parameters:**
   - `channel_id`: (Required) The ID of the target channel (string or integer).
   - `content`: (Optional) Text message content with markdown support (see below).
   - `title`: (Optional) The title of the embed.
   - `image`: (Optional) URL for a large image within the embed.

   **Supported Markdown in `content`:**
   - Headings: `# Heading 1`, `## Heading 2`, etc. (only first level renders properly)
   - Text formatting: `**bold**`, `*italic*`, `__underline__`, `~~strikethrough~~`
   - Block quotes: `> quoted text`
   - Lists: Bullet points with `-` and numbered lists with `1.`, `2.`, etc.
   - Nested lists: Indent with spaces for nested bullets
   - Links: `[link text](https://example.com)`

   **WARNING:** Parameters like `thumbnail`, `description`, `color`, `footer`, and `fields` are **NOT supported** and will cause errors. To create formatted messages, use markdown within the `content` parameter instead.

#### 4.6.3 Disabling Private Mode for Embeds

Nighty's "private mode" can block outgoing messages like embeds — especially when the script pulls from external sources.  
To ensure your embed sends successfully, **temporarily disable private mode** during the send.

```python
# Backup current private mode setting (could be True, False, or None)
current_private = getConfigData().get("private")

# Disable private mode
updateConfigData("private", False)

try:
    # Send the embed
    await forwardEmbedMethod(
        channel_id=ctx.channel.id,
        content="Your embed content",
        title="Your Embed Title"
    )
except Exception as e:
    print(f"Failed to send embed: {e}", type_="ERROR")
finally:
    # Always restore the original private setting (even if it was None)
    updateConfigData("private", current_private)
```

### 4.7 Webhook Integration

Send messages, including complex embeds, to Discord webhooks using the `requests` library. Remember to run synchronous requests in a separate thread.

```python
import requests
import json
import asyncio
from datetime import datetime

# --- Asynchronous Helper (Required for requests) ---
async def run_in_thread(func, *args, **kwargs):
    """Runs a synchronous function in a separate thread."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

# --- Webhook Sending Function ---
def send_webhook_message(webhook_url: str, embed_data: dict = None, content: str = None, username: str = None, avatar_url: str = None) -> bool:
    """
    Sends a message or embed to a Discord webhook.

    Args:
        webhook_url: The URL of the Discord webhook.
        embed_data: A dictionary representing the embed structure.
        content: Plain text message content.
        username: Custom username for the webhook message.
        avatar_url: Custom avatar URL for the webhook message.

    Returns:
        True if the message was sent successfully (HTTP 204), False otherwise.
    """
    if not webhook_url:
        print("Webhook URL is not configured.", type_="ERROR")
        return False
    if not embed_data and not content:
        print("Webhook requires either content or embed data.", type_="ERROR")
        return False

    payload = {}
    if content:
        payload["content"] = content
    if embed_data:
        # Ensure embed_data is properly structured if provided
        payload["embeds"] = [embed_data]
    if username:
        payload["username"] = username
    if avatar_url:
        payload["avatar_url"] = avatar_url

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)

        # Discord typically returns 204 No Content for successful webhook posts
        if response.status_code == 204:
            print("Webhook message sent successfully.", type_="INFO")
            return True
        else:
            # This case might be less common if raise_for_status is used
            print(f"Webhook returned unexpected status: {response.status_code} {response.text}", type_="ERROR")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook message: {e}", type_="ERROR")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during webhook sending: {e}", type_="ERROR")
        return False


# --- Example Usage within an async function (e.g., command handler) ---
async def command_handler(ctx, *, args: str):
    await ctx.message.delete()

    webhook_url = getConfigData().get("my_script_webhook_url") # Get URL from config
    if not webhook_url:
        await ctx.send("Webhook URL not set. Use `<p>setwebhook <url>`.")
        return

    # Example Embed Data (more complex than forwardEmbedMethod allows)
    example_embed = {
        "title": "Webhook Test Embed",
        "description": f"Triggered by {ctx.author.name}.\nArguments: `{args}`",
        "color": 0x5865F2, # Discord blurple
        "fields": [
            {"name": "Server", "value": ctx.guild.name if ctx.guild else "DM", "inline": True},
            {"name": "Channel", "value": ctx.channel.name if ctx.guild else "DM", "inline": True}
        ],
        "footer": {"text": "Sent via NightyScript Webhook"},
        "timestamp": datetime.utcnow().isoformat()
    }

    # Send the embed using the helper function wrapped in run_in_thread
    success = await run_in_thread(
        send_webhook_message,
        webhook_url=webhook_url,
        embed_data=example_embed,
        username="My Script Logger", # Optional custom username
        # avatar_url="...", # Optional custom avatar
        # content="Optional text outside embed" # Optional text
    )

    if success:
        await ctx.send("Message sent to webhook successfully.", delete_after=5)
    else:
        await ctx.send("Failed to send message to webhook.")

# --- Command to set the webhook URL ---
@bot.command(name="setwebhook", description="Set the webhook URL for this script.")
async def set_webhook(ctx, *, url: str):
    await ctx.message.delete()
    if url.startswith("https://discord.com/api/webhooks/"):
        updateConfigData("my_script_webhook_url", url)
        await ctx.send("Webhook URL updated successfully.")
    else:
        await ctx.send("Invalid webhook URL format.")

```

**Best Practices**:

-   **Asynchronous Execution**: **Always** use the `run_in_thread` helper function when calling `requests.post` (or any blocking I/O like file access that isn't inherently async) from within an `async` function (like command handlers or event listeners). This prevents freezing the entire bot.
-   **Error Handling**: Check the return value of `send_webhook_message` or wrap the `run_in_thread` call in `try...except` to handle potential network errors or invalid webhook URLs gracefully. Log errors using `print`.
-   **Configuration**: Store webhook URLs in the Nighty configuration (`getConfigData`/`updateConfigData`) or JSON files, not hardcoded in the script. Provide a command for users to set the URL.
-   **Rate Limits**: Be mindful of Discord's webhook rate limits (generally 30 messages per 60 seconds per channel, but check current Discord developer docs). Avoid spamming webhooks.
-   **Security**: Treat webhook URLs like passwords. Do not expose them publicly. Inform users about the importance of keeping their configured URLs private.

### 4.8 Logging

NightyScript provides a simple logging mechanism using the built-in `print` function with a `type_` argument.

```python
# General informational message (Default level if type_ omitted)
print("Script initialization complete.", type_="INFO")  # Always include type_ parameter
print("Script initialization complete.", type_="INFO")

print(f"Processing item ID: {item_id}", type_="INFO")


# Error message (for critical failures)
print(f"Failed to connect to database: {error_details}", type_="ERROR")

# Success message (for positive confirmation)
print("Configuration saved successfully.", type_="SUCCESS")
```

**Log Levels (`type_` argument):**

-   **`"INFO"`** (Default): General operational information, status updates.
-   **`"ERROR"`**: Reports critical errors that likely prevent part of the script (or the whole script) from functioning correctly.
-   **`"SUCCESS"`**: Confirms that an operation completed successfully (e.g., saving data, completing a task).

> **Note**: The `debug_log` function sometimes seen in older scripts is typically a simple wrapper around this `print` function. It often adds formatting like timestamps or script names. Using `print(message, type_="LEVEL")` directly is the standard approach. Example wrapper:
> ```python
> from datetime import datetime
> SCRIPT_NAME = "MyScript" # Define at script start
> def debug_log(message, type_="INFO"):
>     # Check if debug logging is enabled via config, if desired
>     # is_debug = getConfigData().get(f"{SCRIPT_NAME}_debug_enabled", False)
>     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
>     print(f"[{timestamp}] [{SCRIPT_NAME}] [{type_}] {message}", type_=type_)
> # Usage: debug_log("User command executed", type_="INFO")
> ```

#### 4.8.1 Advanced Error Logging

For more structured logging, especially in complex scripts, implement helper functions.

```python
import traceback
from datetime import datetime

# Define script name for context
SCRIPT_NAME = "MyAdvancedScript"

def is_debug_enabled():
    """Checks if debug logging is enabled in config."""
    try:
        # Assumes a config key like "MyAdvancedScript_debug_enabled"
        return getConfigData().get(f"{SCRIPT_NAME}_debug_enabled", False)
    except Exception as e:
        # Fallback print if getConfigData fails during check
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{SCRIPT_NAME}] [ERROR] Error checking debug status: {e}", type_="ERROR")
        return False

def script_log(message, level="INFO", exc_info=False):
    """
    Logs a message with timestamp, script name, and level.
    Optionally includes exception traceback.

    Args:
        message (str): The message to log.
        level (str): Log level ('INFO', 'ERROR', 'SUCCESS').
        exc_info (bool): If True, appends traceback of current exception.
    """
    level = level.upper()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{SCRIPT_NAME}] [{level}] {message}"

    if exc_info:
        # Append traceback if requested and an exception exists
        exc_text = traceback.format_exc()
        if exc_text and exc_text != 'NoneType: None\n': # Only add if there's a traceback
             log_entry += f"\nTraceback:\n{exc_text}"

    # Use the standard print function with type_ parameter
    print(log_entry, type_=level)

# --- Example Usage ---
def some_function():
    script_log("Starting data processing.", level="INFO")
    try:
        user_id = "12345"
        script_log(f"Fetching data for user: {user_id}", level="INFO")
        # Simulate an error
        result = 10 / 0
    except ZeroDivisionError:
        script_log("Caught a division by zero error!", level="ERROR", exc_info=True)
    except Exception as e:
        # Log other unexpected errors with traceback
        script_log(f"An unexpected error occurred: {e}", level="ERROR", exc_info=True)
    finally:
        script_log("Data processing finished.", level="INFO")

# --- Command to toggle debug mode ---
@bot.command(name=f"{SCRIPT_NAME.lower()}_debug", description=f"Toggle debug logging for {SCRIPT_NAME}.")
async def toggle_debug(ctx, *, args: str):
     await ctx.message.delete()
     current_state = is_debug_enabled()
     new_state = not current_state
     updateConfigData(f"{SCRIPT_NAME}_debug_enabled", new_state)
     await ctx.send(f"{SCRIPT_NAME} debug logging {'enabled' if new_state else 'disabled'}.")

# --- Inside your main script_function() ---
# Initialize debug setting if not present
if getConfigData().get(f"{SCRIPT_NAME}_debug_enabled") is None:
     updateConfigData(f"{SCRIPT_NAME}_debug_enabled", False)

# Call the example function (or integrate logging into your script)
# some_function()

```

#### 4.8.2 Best Practices for Logging

1.  **Use Levels Appropriately**: Distinguish between routine info and critical errors.
2.  **Context is Key**: Log relevant variables or state information, especially with errors. "Error occurred" is less helpful than "Error processing user ID 12345: Connection timeout".
3.  **Log Exceptions**: When catching errors, log the exception message (`str(e)`) and consider logging the full traceback (`traceback.format_exc()` or use `exc_info=True` in the helper) for `ERROR` level logs.
4.  **Be Concise but Informative**: Avoid overly verbose logs for `INFO` or `SUCCESS`. Focus on important details.
5.  **Consistency**: Use a consistent format (like the helper function provides) across your script. Prefixing with the script name is vital when multiple scripts are running.
6.  **Avoid Sensitive Data**: Be careful not to log passwords, API keys, or private user information.

## 5. Asynchronous Operations

NightyScript is built on `asyncio`. Blocking operations (like long-running computations, standard file I/O, or network requests using `requests`) will freeze the bot. Always use asynchronous alternatives when possible.

### 5.1 HTTP Requests with aiohttp

**`aiohttp` (NOT Recommended for HTTP Requests):**
   Use `aiohttp` for non-blocking web requests within `async` functions.

   ```python
   import aiohttp
   import asyncio

   async def fetch_data(url):
       headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
       }
       try:
           async with aiohttp.ClientSession(headers=headers) as session:
               async with session.get(url, timeout=10) as response: # Add a timeout
                   response.raise_for_status() # Raise exception for bad status codes
                   # Use await response.json() for JSON, await response.text() for text
                   data = await response.json()
                   script_log(f"Successfully fetched data from {url}", level="INFO")
                   return data
       except aiohttp.ClientError as e:
           script_log(f"aiohttp error fetching {url}: {e}", level="ERROR")
           return None
       except asyncio.TimeoutError:
           script_log(f"Timeout fetching {url}", level="ERROR")
           return None
       except Exception as e:
            script_log(f"Unexpected error fetching {url}: {e}", level="ERROR", exc_info=True)
            return None

   # Usage in a command:
   @bot.command(name="getapi")
   async def get_api_data(ctx, *, api_url: str):
        await ctx.message.delete()
        data = await fetch_data(api_url)
        if data:
            await ctx.send(f"Data received: ```json\n{json.dumps(data, indent=2)[:1900]}```") # Send preview
        else:
            await ctx.send("Failed to fetch data from the API.")

   ```

### 5.2 Using Synchronous Libraries Safely

**`requests` (Use with `run_in_thread`):**
   If you must use the synchronous `requests` library (or another blocking library), wrap the call in `run_in_thread` (defined in Section 4.7 Webhooks).

   ```python
   import requests

   # (run_in_thread definition needed - see Section 4.7)

   def sync_request_function(url):
       headers = {
           "User-Agent": "Mozilla/5.0 ..." # Set User-Agent
       }
       try:
           response = requests.get(url, headers=headers, timeout=10)
           response.raise_for_status()
           return response.json()
       except requests.exceptions.RequestException as e:
           script_log(f"requests error fetching {url}: {e}", level="ERROR") # Use your script_log
           return None

   # Usage in an async command:
   @bot.command(name="getsync")
   async def get_sync_data(ctx, *, api_url: str):
       await ctx.message.delete()
       msg = await ctx.send(f"Fetching data from {api_url}...")
       # Call the synchronous function using the async helper
       data = await run_in_thread(sync_request_function, api_url)
       if data:
           await msg.edit(content=f"Sync data received: ```json\n{json.dumps(data, indent=2)[:1900]}```")
       else:
           await msg.edit(content="Failed to fetch sync data.")
   ```

### 5.3 Non-blocking Delays

**`asyncio.sleep()`:**
   Use `asyncio.sleep(seconds)` instead of `time.sleep(seconds)` for non-blocking pauses within `async` functions.

   ```python
   async def delayed_action(ctx):
       await ctx.send("Action starting...")
       await asyncio.sleep(5) # Wait 5 seconds without blocking
       await ctx.send("Action complete after 5 seconds.")
   ```

### 5.4 Asynchronous File I/O

**Asynchronous File I/O (`aiofiles` - **Not Recommended if Not Built-in**):**
   Standard Python file operations (`open()`, `read()`, `write()`) are blocking. If you need high-performance async file I/O, the `aiofiles` library is standard, *however*, since external packages cannot be installed, rely on `run_in_thread` for file operations if they might block significantly (e.g., writing very large files). For typical config/JSON reads/writes, the blocking time is usually negligible.

   ```python
   import json
   # (run_in_thread definition needed)
   # (load_data / save_data definitions from Section 4.2)

   # Example: Saving large data potentially could block
   async def save_large_data_async(data):
       script_log("Saving large data asynchronously...", level="INFO")
       success = await run_in_thread(save_data, data) # Assuming save_data is the sync function from 4.2
       if success:
           script_log("Large data saved.", level="INFO")
       else:
           script_log("Failed to save large data.", level="ERROR")

   ```

**Key Takeaway**: Identify blocking operations. Use `aiohttp` for web requests. Use `asyncio.sleep` for delays. Wrap other blocking calls (like `requests` or potentially heavy file I/O) in `run_in_thread`.

## 6. Common Script Patterns

NightyScript can be used to create various types of useful scripts:

### 6.1 API Clients
Interact with external web services (weather, stocks, game stats, translation). Use `aiohttp` or `requests`+`run_in_thread`. Store API keys in config.

### 6.2 Auto-Responders/Triggers
Listen for keywords (`on_message`) or reactions (`on_reaction_add`) and perform actions. Use filtering (Section 4.5) heavily.

### 6.3 Event Loggers
Monitor events (`on_message_delete`, `on_message_edit`, `on_voice_state_update`) and log details to a channel (using `forwardEmbedMethod`) or webhook. Use filtering.

### 6.4 Utility Commands
Provide tools for users (e.g., user info lookup, calculations, reminders, managing script settings).

### 6.5 Data Management
Scripts focused on loading, saving, and managing data stored in JSON files, often with commands to add/remove/list items.

### 6.6 User and Member Interaction
Work with specific, accessible users - not global user databases. Due to Discord API limitations (as noted in Section 1), scripts cannot scan across all servers for mutual friends or build comprehensive user databases. Instead, focus on interacting with users who send messages in accessible channels or are explicitly specified by ID.

