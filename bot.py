import discord
from discord import app_commands
from services.chat_service import ChatService
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

load_dotenv()

class CremeBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.chat_service = ChatService()

    async def setup_hook(self):
        await self.tree.sync()
        
    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

client = CremeBot()

@client.tree.command(name="chat", description="Chat with Crème Brûlée")
async def chat(interaction: discord.Interaction, message: str):
    try:
        logger.info(f"Received chat command from {interaction.user}: {message}")
        await interaction.response.defer()
        response = await client.chat_service.generate_response(
            user_id=str(interaction.user.id),
            message=message
        )
        await interaction.followup.send(response["response"])
        logger.info("Successfully sent response")
    except Exception as e:
        logger.error(f"Error in chat command: {str(e)}")
        await interaction.followup.send("Meow? Something went wrong!")

@client.tree.command(name="decree", description="Request a royal decree")
async def decree(interaction: discord.Interaction):
    try:
        logger.info(f"Received decree command from {interaction.user}")
        await interaction.response.defer()
        response = await client.chat_service.generate_response(
            user_id=str(interaction.user.id),
            message="Issue a royal decree!"
        )
        await interaction.followup.send(response["response"])
        logger.info("Successfully sent decree")
    except Exception as e:
        logger.error(f"Error in decree command: {str(e)}")
        await interaction.followup.send("Meow? Something went wrong with the royal decree!")

def run_bot():
    client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    run_bot() 