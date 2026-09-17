from pathlib import Path


def run(ctx):
    # Projede biome ya da prettier ayarı varsa biome.json eklenmez: iki
    # formatter aynı dosyaları farklı biçimler.
    if not any(any(Path(".").glob(g)) for g in ("biome.json*", ".prettierrc*", "prettier.config.*")):
        ctx.copy_files("files")
    ctx.makefile(ctx.dir / "make.mk")
