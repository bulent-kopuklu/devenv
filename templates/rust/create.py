def run(ctx):
    ctx.copy_files("files")
    ctx.makefile(ctx.dir / "make.mk")
    # Sözleşme bileşeninin (buf) kodunu Rust bileşeni build.rs'te üretir.
    ctx.makefile(ctx.templates / "proto" / "make.mk")
    ctx.rules(ctx.dir / "rules.md")
