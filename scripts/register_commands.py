import requests
import json
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")

def register_commands() -> None:
    """Register slash commands with Discord"""
    
    commands = [
        {
            "name": "chat",
            "description": "Chat with Crème Brûlée",
            "options": [
                {
                    "name": "message",
                    "description": "Your message to Crème Brûlée",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "decree",
            "description": "Request a royal decree from Crème Brûlée",
            "type": 1  # CHAT_INPUT
        }
    ]

    url = f"https://discord.com/api/v8/applications/{APPLICATION_ID}/commands"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    # Delete existing commands
    existing_commands = requests.get(url, headers=headers).json()
    for command in existing_commands:
        delete_url = f"{url}/{command['id']}"
        requests.delete(delete_url, headers=headers)

    # Register new commands
    for command in commands:
        response = requests.post(url, headers=headers, json=command)
        if response.status_code == 200:
            print(f"Successfully registered command: {command['name']}")
        else:
            print(f"Failed to register command: {command['name']}")
            print(f"Error: {response.text}")

if __name__ == "__main__":
    register_commands() 