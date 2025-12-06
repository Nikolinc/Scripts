import os
from PIL import Image

QUALITY = 80
DELETE_ORIGINAL = True

def convert_dir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(".png"):
                png_path = os.path.join(root, file)
                webp_path = os.path.splitext(png_path)[0] + ".webp"

                print(f"Конвертирую: {png_path} → {webp_path}")

                try:
                    img = Image.open(png_path).convert("RGBA")
                    img.save(webp_path, "webp", quality=QUALITY)

                    if DELETE_ORIGINAL:
                        os.remove(png_path)
                        print(f"Удалён: {png_path}")

                except Exception as e:
                    print(f"Ошибка: {e}")

    print("\nГотово!")

if __name__ == "__main__":
    folder = input("Введите путь к папке с PNG: ").strip()

    if not os.path.isdir(folder):
        print("Папка не найдена. Проверь путь.")
    else:
        convert_dir(folder)