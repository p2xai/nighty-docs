@nightyScript(
    name="qBittorrent Info",
    author="AutoGPT",
    description="Fetch torrent status from a qBittorrent instance",
    usage="<p>torrents",
)
def qbittorrent_info_script():
    """
    qBittorrent Info
    ----------------

    Fetches the list of torrents from a qBittorrent instance using its Web API.

    COMMANDS:
    <p>torrents - List torrents with their state and progress
    <p>qbconfig get <key> - Get a configuration value (host, username, password)
    <p>qbconfig set <key> <value> - Set a configuration value

    EXAMPLES:
    <p>torrents - Show current torrent status

    NOTES:
    - Requires `requests` package
    - You can either set the values below or use the `qbconfig` command
    - Configuration keys:
        `qb_host` - Base URL of qBittorrent (e.g., http://127.0.0.1:8080)
        `qb_username` - qBittorrent username
        `qb_password` - qBittorrent password
    """

    import requests

    QB_HOST_KEY = "qb_host"
    QB_USER_KEY = "qb_username"
    QB_PASS_KEY = "qb_password"

    # Default values if not configured via `qbconfig`
    DEFAULT_HOST = "http://127.0.0.1:8080"
    DEFAULT_USERNAME = ""
    DEFAULT_PASSWORD = ""

    KEY_MAP = {
        "host": QB_HOST_KEY,
        "username": QB_USER_KEY,
        "password": QB_PASS_KEY,
    }

    @bot.command(name="qbconfig", description="Get or set qBittorrent config")
    async def qbconfig_cmd(ctx, *, args: str):
        await ctx.message.delete()

        parts = args.strip().split(maxsplit=2)
        if len(parts) < 2:
            await ctx.send(
                "Usage: `<p>qbconfig get <host|username|password>` or `<p>qbconfig set <host|username|password> <value>`"
            )
            return

        action = parts[0].lower()
        key = parts[1].lower()

        if key not in KEY_MAP:
            await ctx.send("Invalid key. Use host, username, or password.")
            return

        conf_key = KEY_MAP[key]

        if action == "get":
            value = getConfigData().get(conf_key)
            if value is None:
                if key == "host":
                    value = DEFAULT_HOST
                elif key == "username":
                    value = DEFAULT_USERNAME
                else:
                    value = DEFAULT_PASSWORD
            if key == "password" and value:
                value = "***"
            await ctx.send(f"{key}: {value if value else 'Not set'}")
        elif action == "set":
            if len(parts) < 3:
                await ctx.send("Usage: `<p>qbconfig set <key> <value>`")
                return
            value = parts[2]
            updateConfigData(conf_key, value)
            await ctx.send(f"Set {key}.")
        else:
            await ctx.send("Invalid action. Use 'get' or 'set'.")

    @bot.command(name="torrents", description="List torrents from qBittorrent")
    async def torrents_cmd(ctx):
        await ctx.message.delete()

        conf = getConfigData()
        host = conf.get(QB_HOST_KEY, DEFAULT_HOST).rstrip("/")
        username = conf.get(QB_USER_KEY, DEFAULT_USERNAME)
        password = conf.get(QB_PASS_KEY, DEFAULT_PASSWORD)

        if not username or not password:
            await ctx.send(
                "qBittorrent credentials not set. Use `<p>qbconfig set username <user>` and `<p>qbconfig set password <pass>` or edit DEFAULT_USERNAME/DEFAULT_PASSWORD in the script."
            )
            return

        try:
            session = requests.Session()
            login_resp = session.post(
                f"{host}/api/v2/auth/login",
                data={"username": username, "password": password},
                timeout=10,
            )
            if login_resp.status_code != 200 or login_resp.text != "Ok.":
                await ctx.send(
                    f"Login failed (status {login_resp.status_code}). Check credentials."
                )
                return

            resp = session.get(f"{host}/api/v2/torrents/info", timeout=10)
            if resp.status_code != 200:
                await ctx.send(f"Failed to fetch torrents (status {resp.status_code}).")
                return

            torrents = resp.json()
            if not torrents:
                await ctx.send("No torrents found.")
                return

            lines = []
            for t in torrents:
                name = t.get("name", "Unnamed")
                state = t.get("state", "unknown")
                progress = t.get("progress", 0) * 100
                lines.append(f"{name} ({state}) - {progress:.1f}%")
            output = "\n".join(lines)
            if len(output) > 1900:
                output = output[:1900] + "..."
            await ctx.send(f"qBittorrent Torrents:\n```\n{output}\n```")
        except Exception as e:
            await ctx.send(f"Error: {e}")

qbittorrent_info_script()
