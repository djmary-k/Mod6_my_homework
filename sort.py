# Скрипт повинен проходити по вказаній під час виклику папці та сортирувати всі файли за групами:
# - зображення ('JPEG', 'PNG', 'JPG', 'SVG');
# - відео файли ('AVI', 'MP4', 'MOV', 'MKV');
# - документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
# - музика ('MP3', 'OGG', 'WAV', 'AMR');
# - архіви ('ZIP', 'GZ', 'TAR');
# - невідомі розширення.

# В результатах роботи повинні бути:
# - Список файлів в кожній категорії (музика, відео, фото та ін.)
# - Перелік усіх відомих скрипту розширень, які зустрічаються в цільовій папці.
# - Перелік всіх розширень, які скрипту невідомі.

import sys
from pathlib import Path

# images - зображення ('JPEG', 'PNG', 'JPG', 'SVG')
IMAGES = []
# JPEG_IMAGES = []
# JPG_IMAGES = []
# PNG_IMAGES = []
# SVG_IMAGES = []
# video - відео файли ('AVI', 'MP4', 'MOV', 'MKV')
VIDEO = []
# AVI_VIDEO = []
# MP4_VIDEO = []
# MOV_VIDEO = []
# MKV_VIDEO = []
# documents - документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
DOCS = []
# DOC_DOCS = []
# DOCX_DOCS = []
# TXT_DOCS = []
# PDF_DOCS = []
# XLSX_DOCS = []
# PPTX_DOCS = []
# audio - музика ('MP3', 'OGG', 'WAV', 'AMR')
AUDIO = []
# MP3_AUDIO = []
# OGG_AUDIO = []
# WAV_AUDIO = []
# AMR_AUDIO = []
# archives - архіви ('ZIP', 'GZ', 'TAR')
ARCHIVES = []
# ZIP_ARCHIVES = []
# GZ_ARCHIVES = []
# TAR_ARCHIVES = []
# others - невідомі розширення
OTHERS = []
# others = []


REGISTER_EXTENSION = {
    'JPEG': IMAGES,
    'JPG': IMAGES,
    'PNG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO,
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCS,
    'DOCX': DOCS,
    'TXT': DOCS,
    'PDF': DOCS,
    'XLSX': DOCS,
    'PPTX': DOCS,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()  # перетворюємо розширення файлу на назву папки jpg -> JPG

def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її до списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією в яку ми складаємо вже файли
            if item.name not in ('images', 'video', 'documents', 'audio', 'archives', 'others'):
                FOLDERS.append(item)
                # скануємо вкладену папку
                scan(item)  # рекурсія
            continue  # переходимо до наступного елементу в сканованій папці

        #  Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        # ext = item.name.suffix[1:]
        fullname = folder / item.name  # беремо шлях до файлу
        if not ext:  # якщо файл немає розширення то додаєм до невідомих
            OTHERS.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не зареєстрували розширення у REGISTER_EXTENSION, то додаємо до невідомих
                UNKNOWN.add(ext)
                OTHERS.append(fullname)


if __name__ == "__main__":
    folder_to_scan = sys.argv[1] # py sort.py garbage
    print(f'Start in folder {folder_to_scan}')
    scan(Path(folder_to_scan))
    print(f'Images files: {IMAGES}')
    print(f'Videos files: {VIDEO}')
    print(f'Documents files: {DOCS}')
    print(f'Audio files: {AUDIO}')
    print(f'Archives files: {ARCHIVES}')

    print(f'Types of files in folder: {EXTENSION}')
    print(f'Unknown types of files: {UNKNOWN}') # невідомі типи файлів
    print(f'OTHERS: {OTHERS}') # папка з невідомими файлами

    # print(f'FOLDERS: {FOLDERS}')
