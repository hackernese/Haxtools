import os
import shutil


def make_dir_if_not_exist(d: str) -> None:
    """Make a directory if not already exists
    Args:
        d (string): path of the directory
    """
    try:
        os.mkdir(d)
    except FileExistsError:
        pass


def copy_if_not_exist(src: str, des: str) -> None:
    if os.path.isfile(des):
        return
    shutil.copyfile(src, des)
