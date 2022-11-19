import os


def create_folder_os(newpath: str) -> None:
    if not os.path.exists(newpath):
        os.makedirs(newpath)
