"""
    Commands:
        hack -toolset=<name>    : Open up a toolset
        hack -toolset=<name> -n : Provide the name of the toolset
        hack -toolset=<name> --add=<new command> : Register a new tool to easily startup
        hack -toolset=<name> --del=<new command> : Unregister a tool from the toolset
        hack -toolset=<name> -l : List all existing toolset
        hack -toolset=<name> -r : Delete a specific toolset
"""

from constant import *
from utils import *
from logs import *
import os
import json
import pprint


def toolset(args):

    # Check if this is a new setip
    if "toolsets" not in CONFIGURATION:
        print("New setup detected, setting toolsets in configuration", warning=True)
        CONFIGURATION["toolsets"] = {}
        json.dump(CONFIGURATION, open(CONFIG_PATH, "r+"), indent=4)

    if args.toolset not in CONFIGURATION["toolsets"]:
        if not args.new:
            print(
                f'Unable to find toolset with the name of "{args.toolset}". To create a new toolset, include the "-n" flag',
                error=True,
            )
            os._exit(1)

        CONFIGURATION["toolsets"][args.toolset] = []
        json.dump(CONFIGURATION, open(CONFIG_PATH, "r+"), indent=4)
        print(f'Successfully created new toolset "{args.toolset}"', ok=True)

    if args.remove:
        # Remove the toolset
        del CONFIGURATION["toolsets"][args.toolset]
        json.dump(CONFIGURATION, open(CONFIG_PATH, "w"), indent=4)
        print(f'Successfully deleted toolset "{args.toolset}"', ok=True)
        os._exit(0)

    # print(constant.CONFIGURATION)
    # print(args.toolset)
