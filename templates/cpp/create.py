def run(ctx):
    ctx.defaults()
    ctx.copy_files("init", dest=f"components/{ctx.project}", replace={"PROJECT_NAME": ctx.project})
