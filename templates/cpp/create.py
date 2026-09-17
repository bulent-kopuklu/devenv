from pathlib import Path


def run(ctx):
    ctx.defaults()
    # Boş projede ilk bileşen: components/<proje adı>/. Bileşeni olan projeye
    # (var olan repo) kaynak dosyası eklenmez.
    if not Path("components").exists():
        ctx.copy_files("init", dest=f"components/{ctx.project}", replace={"PROJECT_NAME": ctx.project})
