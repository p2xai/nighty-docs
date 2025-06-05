@nightyScript(
    name="Server Channel Selector",
    author="thedorekaczynski",
    description="Demonstrates server and channel selection in UI",
    usage="Use the UI to select servers and channels"
)
def server_channel_selector():
    """
    Server Channel Selector
    ---------------------
    
    This script demonstrates how to create a UI for selecting servers and channels.
    It shows how to dynamically update channel options based on the selected server.
    
    COMMANDS:
    None - This script is controlled entirely through the UI
    
    EXAMPLES:
    None - This script is controlled entirely through the UI
    
    NOTES:
    - This script creates a custom tab in Nighty's interface
    - The tab allows you to select a server and then a channel from that server
    - The channel selection is dynamically updated based on the selected server
    """
    
    # Create the main tab
    tab = Tab(name="Server Channel Selector", title="Server and Channel Selection", icon="message")
    
    # Create the main container
    main_container = tab.create_container(type="columns")
    
    # Create the card for server and channel selection
    card = main_container.create_card(gap=4)
    card.create_ui_element(UI.Text, content="Server and Channel Selection", size="lg", weight="bold")
    
    # Create server selection section
    server_section = card.create_group(type="rows", gap=4, full_width=True)
    server_section.create_ui_element(UI.Text, content="Server Selection", size="base", weight="bold")
    
    # Create server selection dropdown
    servers_select_list = [{"id": "select_server", "title": "Select server"}]
    for server in bot.guilds:
        server_row = {"id": str(server.id), "title": server.name, "iconUrl": "https://cdn.discordapp.com/embed/avatars/0.png"}
        if server.icon:
            server_row = {"id": str(server.id), "title": server.name, "iconUrl": server.icon.url}
        servers_select_list.append(server_row)
    
    # Create server selection group
    server_select_group = server_section.create_group(type="rows", gap=2, full_width=True)
    
    # Create server select dropdown
    server_select = server_select_group.create_ui_element(
        UI.Select,
        label="Select a server",
        items=servers_select_list,
        disabled_items=["select_server"],
        mode="single",
        full_width=True
    )
    
    # Create channel selection section
    channel_section = card.create_group(type="rows", gap=4, full_width=True)
    channel_section.create_ui_element(UI.Text, content="Channel Selection", size="base", weight="bold")
    
    # Create channel selection group
    channel_select_group = channel_section.create_group(type="rows", gap=2, full_width=True)
    
    # Create channel select dropdown (initially hidden)
    channel_select = channel_select_group.create_ui_element(
        UI.Select,
        label="Select a channel",
        items=[{"id": "channel_select", "title": "Select channels"}],
        disabled_items=["channel_select"],
        mode="single",
        full_width=True,
        visible=False
    )
    
    # Create status display
    status_section = card.create_group(type="rows", gap=4, full_width=True)
    status_section.create_ui_element(UI.Text, content="Selection Status", size="base", weight="bold")
    
    status_text = status_section.create_ui_element(
        UI.Text,
        content="No server or channel selected",
        size="base",
        color="#f87171"
    )
    
    # Function to update channels based on selected server
    def updateChannels(selected):
        if not selected:
            channel_select.visible = False
            status_text.content = "No server selected"
            status_text.color = "#f87171"
            return
            
        # Get the selected server
        server_id = selected[0]
        server = bot.get_guild(int(server_id))
        
        if not server:
            channel_select.visible = False
            status_text.content = f"Server with ID {server_id} not found"
            status_text.color = "#f87171"
            return
            
        # Update status text
        status_text.content = f"Selected server: {server.name}"
        status_text.color = "#4ade80"
        
        # Create channel list for the selected server
        channel_select_list = [{"id": "channel_select", "title": "Select channels"}]
        for channel in server.text_channels:
            if channel.permissions_for(server.me).send_messages:
                channel_row = {"id": str(channel.id), "title": channel.name}
                channel_select_list.append(channel_row)
                
        # Update channel select dropdown
        channel_select.items = channel_select_list
        channel_select.visible = True
    
    # Function to update status when a channel is selected
    def updateChannelStatus(selected):
        if not selected or selected[0] == "channel_select":
            status_text.content = "No channel selected"
            status_text.color = "#f87171"
            return
            
        # Get the selected channel
        channel_id = selected[0]
        channel = bot.get_channel(int(channel_id))
        
        if not channel:
            status_text.content = f"Channel with ID {channel_id} not found"
            status_text.color = "#f87171"
            return
            
        # Update status text
        status_text.content = f"Selected server: {server_select.selected_items[0]}, Channel: #{channel.name}"
        status_text.color = "#4ade80"
    
    # Set up event handlers
    server_select.onChange = updateChannels
    channel_select.onChange = updateChannelStatus
    
    # Render the tab
    tab.render()

server_channel_selector()  # Call to initialize 