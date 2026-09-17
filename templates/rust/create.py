from pathlib import Path


def run(ctx):
    # rustfmt iki adı da okur; projede biri varsa ikincisi eklenmez.
    if not Path(".rustfmt.toml").exists():
        ctx.copy_files("files")
    ctx.makefile(ctx.dir / "make.mk")
    # Sözleşme bileşeninin (buf) kodunu Rust bileşeni build.rs'te üretir.
    ctx.makefile(ctx.templates / "proto" / "make.mk")
    ctx.rules(ctx.dir / "rules.md")
