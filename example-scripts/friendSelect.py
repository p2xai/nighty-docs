@nightyScript(
    name="Friend Select",
    author="thedorekaczynski",
    description="Select a friend from a dropdown menu.",
    usage="Select the friend from the selection menu on the custom tab."
)
def friendSelect():
    """
    FRIEND SELECT
    ----------
    
    A UI script that allows selecting friends from a dropdown menu.
    The selected friend's ID is stored in a JSON file for use by other scripts.
    
    USAGE:
    Select a friend from the dropdown menu in the Friend Select tab.
    """
    import os
    import json
    from pathlib import Path
    
    # Create script data directory if it doesn't exist
    os.makedirs(f'{getScriptsPath()}/scriptData', exist_ok=True)
    script_config_path = f"{getScriptsPath()}/scriptData/friendSelect.json"
    
    # Initialize the config file if it doesn't exist
    if not os.path.exists(script_config_path):
        with open(script_config_path, 'w', encoding="utf-8") as f:
            json.dump({"selected_friend": None}, f, indent=2)
    
    def updateSetting(key, value):
        """Update a setting in the config file"""
        try:
            with open(script_config_path, 'r', encoding="utf-8", errors="ignore") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}
        
        config[key] = value
        
        with open(script_config_path, 'w', encoding="utf-8", errors="ignore") as f:
            json.dump(config, f, indent=2)

    def getSetting(key=None):
        """Get a setting from the config file"""
        try:
            with open(script_config_path, 'r', encoding="utf-8", errors="ignore") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None if key else {}
        
        if key:
            return config.get(key)
        return config

    def updateSelectedFriend(selected: list):
        """Update the selected friend in the config file"""
        updateSetting("selected_friend", selected)

    # Create list of friends for the select menu
    friends_select_list = [{"id": "select_friend", "title": "Select friend"}]
    
    # Get all users the bot has DMs with
    for channel in bot.private_channels:
        if channel.recipient:
            friend = channel.recipient
            friend_row = {"id": str(friend.id), "title": friend.name, "iconUrl": "https://cdn.discordapp.com/embed/avatars/0.png"}
            if hasattr(friend, 'avatar') and friend.avatar:
                friend_row = {"id": str(friend.id), "title": friend.name, "iconUrl": friend.avatar.url}
            friends_select_list.append(friend_row)

    # Create the UI
    select_tab = Tab(name='Friend Select', title="Friend Selection", icon="heart")
    select_container = select_tab.create_container(type="rows")
    select_card = select_container.create_card(height="full", width="full", gap=3)
    
    # Add description text
    select_card.create_ui_element(UI.Text,
        content="Select a friend from the dropdown menu below:",
        size="base",
        weight="bold",
        color="white",
        align="left"
    )
    
    # Add friend selection dropdown
    select_card.create_ui_element(UI.Select, 
        label="Select friend", 
        full_width=True, 
        selected_items=getSetting("selected_friend"), 
        disabled_items=['select_friend'], 
        mode="single", 
        items=friends_select_list, 
        onChange=updateSelectedFriend
    )

    select_tab.render()

friendSelect() 