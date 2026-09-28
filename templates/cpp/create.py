def run(ctx):
    ctx.defaults()
    # devenv add projenin adini bilmez; iskelet yalniz create'te kurulur.
    if ctx.project:
        ctx.copy_files("init", dest=f"components/{ctx.project}", replace={"PROJECT_NAME": ctx.project})
