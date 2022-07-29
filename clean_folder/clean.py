from clean_folder import file_parser as parser
from clean_folder.normalize import normalize
from pathlib import Path
import shutil
import sys



def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    # Створюємо папку для архіву
    target_folder.mkdir(exist_ok=True, parents=True)
    # Створюємо папку куди розпакуємо архів
    # Беремо суфікс у файла і удаляємо replace(filename.suffix, '')
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))

    # Створюємо папку для архіву з іменем файлу
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Це не архів {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Error delete folder: {folder}')


def main():
    try:
        folder_for_scan = Path(sys.argv[1])
    except Exception:
        print('You enter wrong path to folder')
        sys.exit(1)

    print(f'Start in folder {folder_for_scan.resolve()}')
    parser.scan(folder_for_scan)
    for file in parser.IMAGES:
        handle_media(file, folder_for_scan / 'images')
    for file in parser.DOCUMENTS:
        handle_media(file, folder_for_scan / 'documents')
    for file in parser.AUDIO:
        handle_media(file, folder_for_scan / 'audio')
    for file in parser.VIDEO:
        handle_media(file, folder_for_scan / 'video')

    for file in parser.MY_OTHER:
        handle_other(file, folder_for_scan / 'my_other')
    for file in parser.ARCHIVES:
        handle_archive(file, folder_for_scan / 'archives')

    # Виконуємо реверс списку для того щоб видалити всі папки
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

