import re
import os
import json
import signal
import webbrowser
import subprocess
import webbrowser



# Simulate a list of available bots
bots = ["coffee_bot", "tea_bot", "juice_bot"]

##-----------------------------
commands = {
    "list bots": "List all available bots.",
    "interact <bot_name>": "Start interacting with a specified bot.",
    "open html ui": "Open the bot's HTML user interface in your default web browser.",
    "open api doc": "Open the API documentation in your default web browser.",
    "exit": "Exit the script.",
    "help": "Display this help message."
}

def display_help():
    print("Available commands:")
    for command, description in commands.items():
        print(f"{command}: {description}")

def list_bots(filter_pattern=""):
    filtered_bots = [bot for bot in bots if re.search(filter_pattern, bot)]
    print("Available bots:", ", ".join(filtered_bots))

def main_functions(bot_name):
    if bot_name == "coffee_bot":
        print("Main functions: Order Coffee, See Menu, Open HTML UI, Exit")
    else:
        print(f"{bot_name} is not supported in this script.")

##-----------------------------
def open_html_ui():
    with open('bot_coffee/bot_config.json') as config_file:
        config = json.load(config_file)
        webbrowser.open(config['ui_path'])

##-----------------------------
# Function to start the Flask app
def start_coffee_api():
    # Ensure the path to coffee_api.py is correct
    coffee_api_path = 'bot_coffee/coffee_api.py'    
    flask_process = subprocess.Popen(['python', coffee_api_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    #flask_process = subprocess.Popen(['python', coffee_api_path], preexec_fn=os.setsid)
    return flask_process
	
# Function to open the API documentation
def open_api_doc():    
    with open('bot_coffee/bot_config.json') as config_file:
        config = json.load(config_file)
        webbrowser.open(config['api_doc_url'])

# Function to stop the Flask app
def stop_coffee_api(flask_process):
    #os.kill(os.getpid(flask_process.pid), signal.SIGTERM)
    flask_process.send_signal(signal.CTRL_BREAK_EVENT)
    flask_process = None


##-----------------------------
def interact_with_bot(bot_name):
    if bot_name not in bots:
        print(f"No bot found with name: {bot_name}")
        return
    
    while True:
        command = input(f"Interacting with {bot_name}. Enter command: ")
        if command == "help":
            display_help()
        elif command == "main functions":
            main_functions(bot_name)
        elif command == "open html ui":
            open_html_ui()
            break  # Exit the interaction loop after opening the UI
        elif command == "exit":
            print("Exiting interaction.")            
            break
        elif command == "open api doc":
            open_api_doc()
        else:
            print("Unknown command.")


##-----------------------------
if __name__ == "__main__":
    list_bots()  # Example: list_bots("^coffee")
    bot_name = input("Enter bot name to interact: ")    
    
    flask_process = start_coffee_api()
    try:        
        interact_with_bot(bot_name)
        pass
    finally:
        stop_coffee_api(flask_process)
