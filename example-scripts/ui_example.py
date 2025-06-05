@nightyScript(
    name="UI Example",
    author="thedorekaczynski",
    description="Demonstrates UI scripting functionality",
    usage="Use the UI to interact with the script"
)
def ui_example():
    """
    UI Example
    ---------
    
    This script demonstrates how to use UI scripting functionality.
    It creates a custom tab with various UI elements.
    
    COMMANDS:
    None - This script is controlled entirely through the UI
    
    EXAMPLES:
    None - This script is controlled entirely through the UI
    
    NOTES:
    - This script creates a custom tab in Nighty's interface
    - The tab contains various UI elements like buttons, inputs, and text
    - The UI is interactive and responds to user actions
    """
    
    # Create a new tab
    tab = Tab(name="UI Example", icon="star", title="UI Example Tab")
    
    # Create top container with two cards side by side
    top_container = tab.create_container(type="columns")
    
    # Create top left and right cards
    top_left_card = top_container.create_card(gap=4)
    top_right_card = top_container.create_card(gap=4)
    
    # Create bottom container with two cards side by side
    bottom_container = tab.create_container(type="columns")
    
    # Create bottom left and right cards
    bottom_left_card = bottom_container.create_card(gap=4)
    bottom_right_card = bottom_container.create_card(gap=4)
    
    # Add content to top left card (header)
    top_left_card.create_ui_element(UI.Text, content="UI Example", size="lg", color="accent")
    
    # Add content to top right card (form)
    top_right_card.create_ui_element(UI.Text, content="Form Example", size="lg", color="primary")
    
    # Create a form group in top right card with column layout for horizontal alignment
    form_group = top_right_card.create_group(type="columns", gap=4, full_width=True)
    
    # Create input fields
    name_input = form_group.create_ui_element(UI.Input, label="Name", placeholder="Enter your name")
    email_input = form_group.create_ui_element(UI.Input, label="Email", placeholder="Enter your email", type="email")
    message_input = form_group.create_ui_element(UI.Input, label="Message", placeholder="Enter your message")
    
    # Create a button group
    button_group = top_right_card.create_group(type="rows", gap=4, horizontal_align="center")
    
    # Create buttons
    submit_button = button_group.create_ui_element(UI.Button, label="Submit", variant="cta")
    clear_button = button_group.create_ui_element(UI.Button, label="Clear", variant="ghost")
    
    # Add content to bottom left card (output)
    bottom_left_card.create_ui_element(UI.Text, content="Output", size="lg", color="primary")
    
    # Create an output text element
    output_text = bottom_left_card.create_ui_element(UI.Text, content="No output yet", size="base", color="secondary")
    
    # Define button click handlers
    def on_submit():
        # Get the input values
        name = name_input.value
        email = email_input.value
        message = message_input.value
        
        # Update the output text
        output_text.content = f"**Name:** {name}\n**Email:** {email}\n**Message:** {message}"
        
        # Show a toast notification
        tab.toast("Form Submitted", "Your form has been submitted successfully.", "SUCCESS")
    
    def on_clear():
        # Clear the input fields
        name_input.value = ""
        email_input.value = ""
        message_input.value = ""
        
        # Update the output text
        output_text.content = "No output yet"
        
        # Show a toast notification
        tab.toast("Form Cleared", "The form has been cleared.", "INFO")
    
    # Set the button click handlers
    submit_button.onClick = on_submit
    clear_button.onClick = on_clear
    
    # Add content to bottom right card (toggle example)
    bottom_right_card.create_ui_element(UI.Text, content="Toggle Example", size="lg", color="primary")
    
    # Create a toggle
    toggle = bottom_right_card.create_ui_element(UI.Toggle, label="Enable Feature")
    
    # Create a status text element
    status_text = bottom_right_card.create_ui_element(UI.Text, content="Feature is disabled", size="base", color="secondary")
    
    # Define toggle change handler
    def on_toggle_change(checked):
        # Update the status text
        status_text.content = f"Feature is {'enabled' if checked else 'disabled'}"
        
        # Show a toast notification
        tab.toast("Toggle Changed", f"Feature is now {'enabled' if checked else 'disabled'}.", "INFO")
    
    # Set the toggle change handler
    toggle.onChange = on_toggle_change
    
    # Add select example directly to bottom right card
    bottom_right_card.create_ui_element(UI.Text, content="Select Example", size="lg", color="primary")
    
    # Create a select dropdown
    select = bottom_right_card.create_ui_element(
        UI.Select,
        label="Select an option",
        items=[
            {"id": "option1", "title": "Option 1"},
            {"id": "option2", "title": "Option 2"},
            {"id": "option3", "title": "Option 3"}
        ],
        mode="single",
        full_width=True
    )
    
    # Create a status text element
    select_status = bottom_right_card.create_ui_element(UI.Text, content="No option selected", size="base", color="secondary")
    
    # Define select change handler
    def on_select_change(selected):
        # Update the status text
        if selected:
            select_status.content = f"Selected: {selected[0]}"
            
            # Show a toast notification
            tab.toast("Option Selected", f"You selected {selected[0]}.", "INFO")
        else:
            select_status.content = "No option selected"
    
    # Set the select change handler
    select.onChange = on_select_change
    
    # Render the tab
    tab.render()

ui_example()  # Call to initialize 