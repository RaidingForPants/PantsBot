from functools import wraps

def toggle_command(func):
    @wraps(func)
    async def with_enable(*args, **kwargs):
        ctx = kwargs['ctx']
        self = kwargs['self']
        if ctx.guild.id in self.disabled_list:
            await ctx.send("This command has been disabled")
        else:
            await func(*args, **kwargs)
    return with_enable
    