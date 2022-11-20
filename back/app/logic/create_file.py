import os
import shutil


def create_folder_os(newpath: str) -> None:
    if not os.path.exists(newpath):
        os.makedirs(newpath)


def delete_folder_os(newpath: str, flag: bool) -> None:
    if flag:
        shutil.rmtree(newpath)
    else:
        os.remove(newpath)


async def save_file_to_uploads(url: str, file, filename: str):
    with open(f'{url}{filename}', "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()


def get_file_size(path: str) -> int:
    return int(os.path.getsize(path))


def check_file_in_folder(path: str) -> bool:
    return os.path.exists(path)
