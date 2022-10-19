import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

default_intents = disnake.Intents.default()
default_intents.members = True
default_intents.message_content = True

bot = commands.InteractionBot(intents=default_intents, sync_commands_debug=True)

@bot.event
async def on_ready():
	print("Connected to Discord")
    
@bot.slash_command(description="Test command")
async def test(inter):
    await inter.response.send_message("Success!")
	
bot.run(TOKEN)