import os
import disnake
import sys
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

default_intents = disnake.Intents.default()
default_intents.members = True
default_intents.message_content = True

bot = commands.InteractionBot(intents=default_intents, sync_commands_debug=True)

def module_exists(module_name):
    return module_name in sys.modules

@bot.event
async def on_ready():
	print("Connected to Discord")
    
@bot.slash_command(description="Test command")
async def test(ctx):
    await ctx.response.send_message("Success!")
    
if module_exists("CogTest"):
    bot.add_cog(CogTest(bot))

if __name__ == "__main__":	
    bot.run(TOKEN)