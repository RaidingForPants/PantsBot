from functools import wraps

def requires_administrator(func):
    @wraps(func)
    async def with_perms(*args, **kwargs):
        ctx = kwargs['ctx']
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You do not have permission to use this command")
        else:
            await func(*args, **kwargs)
    return with_perms
    
def requires_manage_guild(func):
    @wraps(func)
    async def with_perms(*args, **kwargs):
        ctx = kwargs['ctx']
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("You do not have permission to use this command")
        else:
            await func(*args, **kwargs)
    return with_perms