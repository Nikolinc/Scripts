# PNG to WEBP Converter

Этот скрипт автоматически конвертирует все файлы **PNG → WEBP** в
указанной папке (включая вложенные директории).\
После успешной конвертации оригинальные PNG‑файлы удаляются.

## Возможности

-   Рекурсивный обход папок\
-   Конвертация PNG в WEBP с качеством `80`\
-   Автоматическое удаление исходных PNG\
-   Поддержка прозрачности (`RGBA`)

## Структура репозитория

    .
    ├── Python
    │   └── PNG_to_WEBP
    │       ├── png_to_webp.py
    │       └── README.md
    └── windows
        └── Windows Update
            ├── README.md
            └── Reset-WindowsUpdate.ps1

## Как использовать

1.  Установите Pillow:

```{=html}
<!-- -->
```
    pip install pillow

2.  Запустите:

```{=html}
<!-- -->
```
    python png_to_webp.py

3.  Введите путь к папке с PNG.

## Исходный код

https://github.com/Nikolinc/Scripts/blob/main/Python/PNG_to_WEBP/png_to_webp.py
