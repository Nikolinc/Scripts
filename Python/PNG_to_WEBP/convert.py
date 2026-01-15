import os
from PIL import Image

QUALITY = 80
PNG_DIR = input("Путь к папке с PNG: ").strip()
VAULT_DIR = input("Путь к корню проекта: ").strip()
IGNORE_FILE = ".pngignore"
SEARCH_EXTENSIONS = {
    ".md", ".ts", ".tsx", ".js", ".jsx",
    ".py", ".html", ".css", ".scss",
    ".json", ".yml", ".yaml"
}

def load_ignore(path):
    ignore = []
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore.append(line)
    return ignore

IGNORE_LIST = load_ignore(IGNORE_FILE)

def is_ignored(path):
    for item in IGNORE_LIST:
        if item in path:
            return True
    return False

def find_usage(png_name):
    used_in = []
    for root, _, files in os.walk(VAULT_DIR):
        if is_ignored(root):
            continue
        for f in files:
            if os.path.splitext(f)[1].lower() not in SEARCH_EXTENSIONS:
                continue
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as md:
                    if png_name in md.read():
                        used_in.append(path)
            except Exception:
                pass
    return used_in

def convert_png(png_path):
    webp_path = os.path.splitext(png_path)[0] + ".webp"
    img = Image.open(png_path).convert("RGBA")
    img.save(webp_path, "webp", quality=QUALITY)
    return webp_path

def replace_links(md_file, old, new):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    content_new = content.replace(old, new)
    if content != content_new:
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(content_new)
        print(f"{md_file}")

for root, _, files in os.walk(PNG_DIR):
    if is_ignored(root):
        continue
    for file in files:
        if not file.lower().endswith(".png"):
            continue
        png_path = os.path.join(root, file)
        usage = find_usage(file)
        if not usage:
            print(f"{file} → НЕ ИСПОЛЬЗУЕТСЯ")
            os.remove(png_path)
            continue
        print(f"{file} → {len(usage)}")
        webp_path = convert_png(png_path)
        webp_name = os.path.basename(webp_path)
        for md in usage:
            replace_links(md, file, webp_name)
        os.remove(png_path)

print("Готово")