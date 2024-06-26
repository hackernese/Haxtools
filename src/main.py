#!/usr/bin/env ./venv/bin/python
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
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Making your hacking journey more convenient"
    )
    constant.GLOBAL_PARSER = parser

    # Adding required options
    args = set_and_parse_arguments(parser)

    # Running the main service
    p_args = vars(args)
    for arg in p_args:
        if arg in Services and p_args[arg] != None:
            Services[arg]["cmd"](args)


if __name__ == "__main__":
    run()
