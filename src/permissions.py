def requires_administrator(func):
    def with_perms(*args, **kwargs):
        ctx = args[1]
        if not ctx.author.guild_permissions.administrator:
            ctx.send("You do not have permission to use this command")
        else:
            func(*args, **kwargs)
    return with_perms
    
def requires_manage_guild(func):
    def with_perms(*args, **kwargs):
        ctx = args[1]
        if not ctx.author.guild_permissions.manage_guild:
            ctx.send("You do not have permission to use this command")
        else:
            func(*args, **kwargs)
    return with_perms