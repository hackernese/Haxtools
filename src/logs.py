from threading import Thread
from constant import LOG_PATH
import sys
import time
import logging

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

format_bold = (
    lambda msg, color: BOLD
    + (
        Green
        if color == "ok"
        else (
            Red
            if color == "error"
            else Cyan if color == "info" else Yellow if color == "warning" else White
        )
    )
    + msg
    + Reset
)
print_ = print


# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def print(*args, **kwargs):

    if "warning" in kwargs and kwargs["warning"]:
        logging.warning(*args)
        print_("[" + BOLD + Yellow + "WARNING" + Reset + "]:", *args)
    elif "ok" in kwargs and kwargs["ok"]:
        logging.info(*args)
        print_("[" + BOLD + Green + "OK" + Reset + "]:", *args)
    elif "error" in kwargs and kwargs["error"]:
        logging.error(*args)
        print_("[" + BOLD + Red + "ERROR" + Reset + "]:", *args)
    elif "info" in kwargs and kwargs["info"]:
        logging.info(*args)
        print_("[" + BOLD + Cyan + "INFO" + Reset + "]:", *args)
    else:
        logging.debug(*args)
        print_(*args)
        return


# ---- Print loading bar ----
class Loading:

    def __init__(self, msg: str) -> None:
        self.stop_status = None
        self.msg = msg

        self.thread = Thread(target=self.__load)
        self.thread.start()

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

        while self.thread.is_alive():
            time.sleep(0.001)
