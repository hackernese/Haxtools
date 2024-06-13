from constant import APP_DATA, CONFIG_PATH, HTB_PATH, ASSET_PATH
from utils import *
from feature import *
from logs import Loading
import argparse
import os
import sys
import json
import constant


def initialize() -> None:
    # Making startup directories
    make_dir_if_not_exist(APP_DATA)
    make_dir_if_not_exist(HTB_PATH)


def run() -> None:

    initialize()

    # Parsing arguments
    parser = argparse.ArgumentParser(
        description="Making your hacking journey more convenient"
    )

    # Adding required options
    required_group = parser.add_mutually_exclusive_group(required=True)
    required_group.add_argument(
        "-htb",
        choices=["on", "off", "enable"],
        help="Turn on or off HackTheBox service",
    )

    # Optional arguments
    parser.add_argument(
        "--noreg", "--extra_arg", help="Ignore region switching", action="store_true"
    )

    # parsing arguments
    args = parser.parse_args()

    # Running the main service
    for arg in vars(args):
        if arg in Services:
            Services[arg](args)


if __name__ == "__main__":
    run()
