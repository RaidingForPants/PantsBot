import disnake
import sys
from disnake.ext import commands
import environment
import importlib
import colorama
import logger
import permissions

def _try_add_cog(name):
    try:
        importlib.import_module(str(name))
        cog_cls = getattr(sys.modules[name], name)
        logger.log_info("Loaded "+name)
        bot.add_cog(cog_cls(bot))
    except ModuleNotFoundError as err:
        logger.log_error(f"Failed to load cog {name}", err)
        
def _load_cogs():
    logger.log_info("Loading cogs...")
    _try_add_cog("YoutubeCog")
    _try_add_cog("EconomyCog")
    _try_add_cog("GambleCog")
    
def _get_token():
    return environment.TOKEN
    
def _get_intents():
    bot_intents = disnake.Intents.default()
    bot_intents.members = True
    bot_intents.message_content = True
    return bot_intents
        
def start():
    logger.log_info("Starting bot")
    TOKEN = _get_token()
    _load_cogs()
    bot.run(TOKEN)
    
bot = commands.InteractionBot(intents=_get_intents(), sync_commands_debug=True)
log_file_name = None
error_file_name = None
logger = logger.get_instance()



# -------------------- EVENTS START ---------------------

@bot.event
async def on_ready():
    logger.log_info("Connected to Discord")
    
# -------------------- EVENTS END -----------------------




# -------------------- COMMANDS START -------------------

#@bot.slash_command(description="Test command")
#@permissions.requires_administrator
#async def test(ctx):
#    await ctx.send("Success!")

# -------------------- COMMANDS END ---------------------



if __name__ == "__main__":
    colorama.init()
    start()