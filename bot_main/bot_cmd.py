import re
import os
import sys
import json
import signal
import webbrowser
import subprocess
import webbrowser
import javaproperties



def load_properties(filepath):
    with open(filepath, 'r') as file:
        properties = javaproperties.load(file)
    return properties

config = load_properties('./bot_config.properties')
manage_bots = config['manage_bots'].split(',')


##-----------------------------
def load_commands(config):       
    commands_str = config['commands']
    commands_list = [cmd.strip() for cmd in commands_str.split(',')]
    commands_dict = {}
    for cmd in commands_list:
        key, human_friendly, description = cmd.split(':')
        commands_dict[key.strip()] = {"human_friendly": human_friendly.strip(), "description": description.strip()}
    return commands_dict

commands = load_commands(config)


##-----------------------------
def process_input(user_input, commands):
    # Keep words available in the command list only
    keywords = [word for word in user_input.split() if any(word in cmd_info['human_friendly'] for cmd_info in commands.values())]
    
    # Score commands based on match with keywords
    scored_commands = []
    for cmd, cmd_info in commands.items():
        score = sum([1 if keyword in cmd_info['human_friendly'] else 0 for keyword in keywords])
        if score > 0:
            scored_commands.append((score, cmd, cmd_info['human_friendly'], cmd_info['description']))
    
    # Sort by score (high to low)
    scored_commands.sort(reverse=True, key=lambda x: x[0])
    
    # Determine action based on scoring
    if scored_commands:
        if scored_commands[0][0] == len(keywords):  # Perfect match
            execute_command(scored_commands[0][1])
        else:  # Multiple matches or partial match
            print("Did you mean:")
            for _, cmd, human_friendly, _ in scored_commands:
                print(f"- {human_friendly} ({cmd})")
    else:
        display_help(commands)

def display_help(commands):
    print("Available commands:")
    for cmd_info in commands.values():
        print(f"{cmd_info['human_friendly']}: {cmd_info['description']}")

def list_bots(filter_pattern=""):
    filtered_bots = [bot for bot in manage_bots if re.search(filter_pattern, bot)]
    print("Available bots:", ", ".join(filtered_bots))

def run_bot_coffee_cmd():    
    script_path = os.path.join(os.path.dirname(__file__), '..', 'bot_coffee', 'bot_cmd.py')    
    subprocess.run(['python', script_path], check=True)

def execute_command(command):
    print(f"Executing command: {command}")
    if command == "help":
        display_help()
    elif command == "exit":
        print("Exiting interaction.")            
        sys.exist(0)
    elif command == "list_bots":
        list_bots()
    elif command == "get_bot":
        run_bot_coffee_cmd()
    elif command == "open_ui":
        open_html_ui()         
    elif command == "open_api":
        open_api_doc()
    else:
        print("Unknown command.")
        
##-----------------------------
def interact_with_bot(bot_name):
    if bot_name not in manage_bots:
        print(f"No bot found with name: {bot_name}")
        return
    
    while True:
        command = input(f"Interacting with {bot_name}. Enter command: ")                
        process_input(command, commands)

##-----------------------------
if __name__ == "__main__":
    list_bots()  # Example: list_bots("^coffee")
    bot_name = input("Enter bot name to interact: ")    
    interact_with_bot(bot_name)
