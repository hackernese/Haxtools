from threading import Thread
import logging
import sys
import time


# Exit code
JSON_ERROR = -3
UNSUPPORT_OS = -1
COMMAND_NOT_FOUND = -2
UNEXPECTED_ERR = 1

# ANSI color codes
Reset = "\033[0m"
Red = "\033[31m"
Green = "\033[32m"
Yellow = "\033[33m"
Blue = "\033[34m"
Magenta = "\033[35m"
Cyan = "\033[36m"
White = "\033[37m"
RESET = "\033[0m"
BOLD = "\033[1m"


def format_bold(msg, color):
    return BOLD + color + msg + Reset


def print_bold(msg, color):
    sys.stdout.write(FormatColorBold(msg, color))


def log_warning(msg):
    content = "[" + BOLD + Yellow + "WARNING" + Reset + "]:" + msg


def print_info(msg):
    content = "[" + BOLD + Cyan + "INFO" + Reset + "]:" + msg


def print_error(msg):
    content = "[" + BOLD + Red + "ERROR" + Reset + "]:" + msg


def print_ok(msg):
    content = "[" + BOLD + Green + "OK" + Reset + "]:" + msg


# ---- Print loading bar ----
class Loading:

    def __init__(self, msg: str) -> None:
        self.stop_status = None
        self.msg = msg

        Thread(target=self.__load).start()

    def __load(self):
        chars = ["⠋", "⠙", "⠴", "⠦"]
        while self.stop_status == None:
            for c in chars:
                sys.stdout.write(f"{self.msg} {c}\r")
                sys.stdout.flush()
                time.sleep(0.1)

        sys.stdout.write(f"{self.msg} {'✅' if self.stop_status==True else '❌'}\n")
        sys.stdout.flush()

    def stop(self, status: bool):
        self.stop_status = status
