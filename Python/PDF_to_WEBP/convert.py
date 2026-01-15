from pdf2image import convert_from_path
import os

# --- Ввод путей ---
pdf_folder = input("Укажи путь к папке с PDF (например: /path/to/pdf): ").strip()
image_folder = input("Укажи путь к папке для сохранения изображений: ").strip()

# --- Проверки ---
if not os.path.isdir(pdf_folder):
    raise Exception(f"Папка с PDF не найдена: {pdf_folder}")

os.makedirs(image_folder, exist_ok=True)

print(f"\nPDF берём из: {pdf_folder}")
print(f"Изображения сохраняем в: {image_folder}\n")

# --- Конвертация ---
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"Обрабатывается: {pdf_file}")

        images = convert_from_path(
            pdf_path,
            dpi=300
        )

        for i, image in enumerate(images):
            image_name = pdf_file.replace(".pdf", f"_{i+1}.webp")
            output_path = os.path.join(image_folder, image_name)

            image.save(
                output_path,
                "WEBP",
                quality=90,
                method=6
            )

            print(f"  ✔ сохранено: {image_name}")

print("\nГотово. Оригинальные PDF не изменялись.")