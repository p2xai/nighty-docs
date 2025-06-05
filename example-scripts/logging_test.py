@nightyScript(
    name="Logging Test",
    author="thedorekaczynski",
    description="Tests the logging functionality with UI buttons",
    usage="Use the UI to test different log types"
)
def logging_test():
    """
    Logging Test
    -----------
    
    This script demonstrates the logging functionality in NightyScript.
    It provides UI buttons to test different log types.
    
    COMMANDS:
    None - This script uses UI buttons instead of commands
    
    EXAMPLES:
    Click the buttons in the UI to test different log types
    
    NOTES:
    - This script demonstrates INFO, SUCCESS, and ERROR log types
    - Logs will appear in the console
    """
    
    # Create the main tab
    tab = Tab(name="Logging Test", title="Logging Test", icon="message")
    
    # Create the main container
    main_container = tab.create_container(type="columns")
    
    # Create the card for logging buttons
    card = main_container.create_card(gap=4)
    card.create_ui_element(UI.Text, content="Logging Test", size="lg", weight="bold")
    
    # Create a description
    card.create_ui_element(
        UI.Text, 
        content="Click the buttons below to test different log types. Logs will appear in the console.", 
        size="base"
    )
    
    # Create a group for the buttons
    button_group = card.create_group(type="columns", gap=4, horizontal_align="center")
    
    # Create buttons for each log type
    info_button = button_group.create_ui_element(
        UI.Button, 
        label="Test INFO Log", 
        variant="solid", 
        color="primary"
    )
    
    success_button = button_group.create_ui_element(
        UI.Button, 
        label="Test SUCCESS Log", 
        variant="solid", 
        color="success"
    )
    
    error_button = button_group.create_ui_element(
        UI.Button, 
        label="Test ERROR Log", 
        variant="solid", 
        color="danger"
    )
    
    # Create a status text element
    status_text = card.create_ui_element(
        UI.Text, 
        content="No logs generated yet", 
        size="base", 
        color="secondary"
    )
    
    # Define button click handlers
    def on_info_click():
        print("This is an INFO log message", type_="INFO")
        status_text.content = "INFO log generated at " + datetime.now().strftime("%H:%M:%S")
        status_text.color = "primary"
    
    def on_success_click():
        print("This is a SUCCESS log message", type_="SUCCESS")
        status_text.content = "SUCCESS log generated at " + datetime.now().strftime("%H:%M:%S")
        status_text.color = "success"
    
    def on_error_click():
        print("This is an ERROR log message", type_="ERROR")
        status_text.content = "ERROR log generated at " + datetime.now().strftime("%H:%M:%S")
        status_text.color = "error"
    
    # Assign click handlers to buttons
    info_button.onClick = on_info_click
    success_button.onClick = on_success_click
    error_button.onClick = on_error_click
    
    # Render the tab
    tab.render()

# Import datetime for timestamps
from datetime import datetime

# Call the script function to activate it
logging_test() 