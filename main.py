# Умови для обробки:
# - зображення переносимо до папки images
# - документи переносимо до папки documents
# - аудіо файли переносимо до audio
# - відео файли до video
# - архіви розпаковуються та їх вміст переноситься до папки archives

# Критерії приймання завдання
# - всі файли та папки перейменовуються за допомогою функції normalize.
# - розширення файлів не змінюється після перейменування.
# - порожні папки видаляються
# - скрипт ігнорує папки archives, video, audio, documents, images;
# - розпакований вміст архіву переноситься до папки archives у підпапку, названу так само, як і архів, але без розширення в кінці;
# - файли, розширення яких невідомі, залишаються без зміни.

from pathlib import Path
import shutil
import sys
import sort as parser # sort - rename
from normalize import normalize

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True) # создаем папку
    filename.replace(target_folder / normalize(filename.name)) # перейменовуэмо назву файлу

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)
        # filename.replace(folder_for_file / normalize(filename.name))
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    filename.unlink() # удаляє файл

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    parser.scan(folder)
    for file in parser.IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.DOCS:
        handle_media(file, folder / 'documents')
    for file in parser.AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')
    for file in parser.OTHERS:
        handle_media(file, folder / 'others')
    

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder: {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())


# запуск файлу main:  py main.py /Users/Maryna/Desktop/garbage 
# запуск файлу main:  py main.py garbage 
