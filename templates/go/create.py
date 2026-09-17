def run(ctx):
    ctx.defaults()
    # Sözleşme bileşeninin (buf) kodunu Go bileşeni kendi build'inde üretir.
    ctx.makefile(ctx.templates / "proto" / "make.mk")
