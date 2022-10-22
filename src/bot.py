import os
import disnake
import sys
from disnake.ext import commands
from dotenv import load_dotenv
import importlib
    
def _log_info(message):
    message = _info_format(message)
    if log_file_name is None:
        print(message)
    else:
        with open(log_file_name, "a") as f:
            f.write(message)
            f.write("\n")
    
def _log_error(message):
    message = _error_format(message)
    if error_file_name is None:
        print(message)
    else:
        with open(error_file_name, "a") as f:
            f.write(message)
            f.write("\n")
        
def _print_info(message):
    print(_info_format(message))
    
def _print_error(message):
    print(_error_format(message))
    
def _info_format(message):
    return message
    
def _error_format(message):
    return message

def _try_add_cog(name):
    try:
        importlib.import_module(str(name))
        cog_cls = getattr(sys.modules[name], name)
        _print_info("Loaded "+name)
        bot.add_cog(cog_cls(bot))
    except ModuleNotFoundError as err:
        _log_error(message=f"Failed to load cog {name}: {err}")
        
def _load_cogs():
    _log_info("Loading cogs...")
    _try_add_cog("CogFake")
    _try_add_cog("CogTest")
    
def _get_token():
    load_dotenv()
    return os.getenv('DISCORD_TOKEN')
    
def _get_intents():
    bot_intents = disnake.Intents.default()
    bot_intents.members = True
    bot_intents.message_content = True
    return bot_intents
        
def start():
    TOKEN = _get_token()
    _load_cogs()
    bot.run(TOKEN)
    
bot = commands.InteractionBot(intents=_get_intents(), sync_commands_debug=True)
log_file_name = None
error_file_name = None

# -------------------- EVENTS START ---------------------

@bot.event
async def on_ready():
	_print_info("Connected to Discord")
    
# -------------------- EVENTS END -----------------------




# -------------------- COMMANDS START -------------------

@bot.slash_command(description="Test command")
async def test(ctx):
    await ctx.response.send_message("Success!")

# -------------------- COMMANDS END ---------------------



if __name__ == "__main__":	
    start()