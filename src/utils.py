from prettytable import PrettyTable

from logs import format_bold
import os
import shutil


class PrintTable:

    def __init__(self, *args, **kwargs) -> None:
        self.table = PrettyTable()
        self.table.field_names = args
        self.rows = []
        self.no_bold_first_column = "nobold" in kwargs and kwargs["nobold"]

    def add(self, *args):
        args_list = list(args)
        args_list[0] = (
            str(args[0])
            if self.no_bold_first_column
            else format_bold(str(args[0]), "ok")
        )
        self.rows.append(args_list)
        return self

    def display(self):
        self.table.add_rows(self.rows)
        self.table.align = "l"
        print(self.table)


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
