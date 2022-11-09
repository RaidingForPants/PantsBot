from functools import wraps

def toggle_command(func):
    @wraps(func)
    async def with_enable(*args, **kwargs):
        ctx = kwargs['ctx']
        self = kwargs['self']
        if not self.enabled:
            await ctx.send("This command has been disabled")
        else:
            await func(*args, **kwargs)
    return with_enable
    
def toggle_listener(func):
    @wraps(func)
    async def with_enable(*args, **kwargs):
        self = args[0]
        if self.enabled:
            await func(*args, **kwargs)
    return with_enable