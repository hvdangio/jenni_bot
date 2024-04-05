import re
import os
import json
import signal
import webbrowser
import subprocess
import webbrowser
import javaproperties


##-----------------------------
commands = {        
    "open html ui": "Open the bot's HTML user interface in your default web browser.",
    "open api doc": "Open the API documentation in your default web browser.",
    "exit": "Exit the script.",
    "help": "Display this help message."
}

def display_help():
    print("Available commands:")
    for command, description in commands.items():
        print(f"{command}: {description}")

def load_properties(filepath):
    with open(filepath, 'r') as file:
        properties = javaproperties.load(file)
    return properties
    
##-----------------------------
def open_html_ui():
    config = load_properties('./bot_config.properties')
    webbrowser.open(config['bot.ui.path'])

##-----------------------------
# Function to start the Flask app
def start_api():
    # Ensure the path to coffee_api.py is correct
    bot_api_path = './bot_api.py'    
    flask_process = subprocess.Popen(['python', bot_api_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    #flask_process = subprocess.Popen(['python', bot_api_path], preexec_fn=os.setsid)
    return flask_process
	
# Function to open the API documentation
def open_api_doc():    
    config = load_properties('./bot_config.properties')   
    webbrowser.open(config['bot.api.doc.url'])
    
# Function to stop the Flask app
def stop_api(flask_process):
    #os.kill(os.getpid(flask_process.pid), signal.SIGTERM)
    flask_process.send_signal(signal.CTRL_BREAK_EVENT)
    flask_process = None


##-----------------------------
def interact_with_bot(bot_name):
    while True:
        command = input(f"Interacting with {bot_name}. Enter command: ")
        if command == "help":
            display_help()  
        elif command == "exit":
            print("Exiting interaction.")            
            break            
        elif command == "open html ui":
            open_html_ui()
            break        
        elif command == "open api doc":
            open_api_doc()
        else:
            print("Unknown command.")


##-----------------------------
if __name__ == "__main__":    
    bot_name = "bot_coffee"    
    flask_process = start_api()
    try:        
        interact_with_bot(bot_name)
        pass
    finally:
        stop_api(flask_process)

