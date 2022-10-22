import os
import disnake
import sys
from disnake.ext import commands
from dotenv import load_dotenv
import importlib
#import CogTest

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

default_intents = disnake.Intents.default()
default_intents.members = True
default_intents.message_content = True

bot = commands.InteractionBot(intents=default_intents, sync_commands_debug=True)

def module_exists(module_name):
    return module_name in sys.modules
    
def _print_error(message, err):
    print(message)
    
def _try_add_cog(name):
    try:
        cog_cls = getattr(sys.modules[name], name)
        bot.add_cog(cog_cls(bot))
    except KeyError as err:
        if importlib.import_module(str(name)) is None:
            _print_error("Failed to load cog "+str(name)+"! ", err)
        else:
            pass
            cog_cls = getattr(sys.modules[name], name)
            print("Loaded "+name)
            bot.add_cog(cog_cls(bot))

@bot.event
async def on_ready():
	print("Connected to Discord")
    
@bot.slash_command(description="Test command")
async def test(ctx):
    await ctx.response.send_message("Success!")
    
_try_add_cog("CogTest")

if __name__ == "__main__":	
    bot.run(TOKEN)