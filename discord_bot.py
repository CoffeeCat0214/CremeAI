import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiohttp
import json

load_dotenv()

class CremeBruleeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.api_url = os.getenv("CHATBOT_API_URL")

    async def setup_hook(self):
        await self.add_cog(ChatCommands(self))

    async def on_ready(self):
        print(f"{self.user} has arrived to their royal chamber!")

class ChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chat")
    async def chat(self, ctx, *, message: str):
        async with aiohttp.ClientSession() as session:
            payload = {
                "user_id": str(ctx.author.id),
                "message": message,
                "platform": "discord"
            }
            
            async with session.post(self.bot.api_url + "/chat", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    await ctx.reply(data["response"])
                    
                    if data.get("decree"):
                        # Format decree in a fancy way
                        decree_embed = discord.Embed(
                            title="🔰 Royal Decree 🔰",
                            description=data["decree"],
                            color=discord.Color.gold()
                        )
                        await ctx.send(embed=decree_embed)
                else:
                    await ctx.reply("*Hisses* Something went wrong with my royal communication channels!")

    @commands.command(name="decree")
    async def decree(self, ctx):
        message = "I demand a royal decree!"
        await self.chat(ctx, message=message)

def run_bot():
    bot = CremeBruleeBot()
    bot.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    run_bot() 