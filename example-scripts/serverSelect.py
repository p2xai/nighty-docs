@nightyScript(
    name="Server Select",
    author="for FReSh",
    description="Select a server from a dropdown menu.",
    usage="Select the server from the selection menu on the custom tab."
)
def serverSelect():
    os.makedirs(f'{getScriptsPath()}/scriptData', exist_ok=True)
    script_config_path = f"{getScriptsPath()}/scriptData/serverSelect.json"
    
    def updateSetting(key, value):
        json.dump({**(json.load(open(script_config_path, 'r', encoding="utf-8", errors="ignore")) if os.path.exists(script_config_path) else {}), key: value}, open(script_config_path, 'w', encoding="utf-8", errors="ignore"), indent=2)

    def getSetting(key=None):
        return (lambda p: (settings := json.load(open(p, 'r', encoding="utf-8", errors="ignore"))) and settings.get(key) if key else settings)(script_config_path) if os.path.exists(script_config_path) else (None if key else {})

    def updateSelectedServer(selected: list):
        updateSetting("selected_server", selected)

    # Create list of servers for the select menu
    servers_select_list = [{"id": "select_server", "title": "Select server"}]
    for server in bot.guilds:
        server_row = {"id": str(server.id), "title": server.name, "iconUrl": "https://cdn.discordapp.com/embed/avatars/0.png"}
        if server.icon:
            server_row = {"id": str(server.id), "title": server.name, "iconUrl": server.icon.url}
        servers_select_list.append(server_row)

    # Create the UI
    select_tab = Tab(name='Server Select', title="Server Selection", icon="users")
    select_container = select_tab.create_container(type="rows")
    select_card = select_container.create_card(height="full", width="full", gap=3)
    
    # Add description text
    select_card.create_ui_element(UI.Text,
        content="Select a server from the dropdown menu below:",
        size="base",
        weight="bold",
        color="white",
        align="left"
    )
    
    # Add server selection dropdown
    select_card.create_ui_element(UI.Select, 
        label="Select server", 
        full_width=True, 
        selected_items=getSetting("selected_server"), 
        disabled_items=['select_server'], 
        mode="single", 
        items=servers_select_list, 
        onChange=updateSelectedServer
    )

    select_tab.render()

serverSelect() 