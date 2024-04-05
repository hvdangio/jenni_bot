import json
import os

def update_ui_path_in_config():
    # Get the absolute path to the bot_coffee directory
    bot_coffee_dir = os.path.abspath('./bot_coffee')
    # Construct the absolute path to ui/index.html
    ui_index_path = os.path.join(bot_coffee_dir, 'ui', 'index.html')       
    
    # Define the path to bot_config.json inside the bot_coffee folder
    config_path = os.path.join(bot_coffee_dir, 'bot_config.json')
    
    # Read the current configuration
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    # Update the ui_path with the absolute path to index.html
    config['ui_path'] = ui_index_path
    
    # Optionally, update the API documentation URL if needed
    # config['api_doc_url'] = 'your_api_doc_url_here'
    
    # Write the updated configuration back to bot_config.json
    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)

# Call the function to update the config
update_ui_path_in_config()
