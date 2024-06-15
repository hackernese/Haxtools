"""
    Commands:
        hack -toolset=<name>    : Open up a toolset

        hack -toolset=<name> -n : Provide the name of the toolset
        hack -toolset=<name> -r : Delete a specific toolset
        hack -toolset=<name> -l : List all existing toolset

        hack -toolset=<name> --add=<new command> : Register a new tool to easily startup
        hack -toolset=<name> --del=<new command> : Unregister a tool from the toolset
"""

from constant import *
from utils import *
from logs import *
import os
import json
import pprint
import shutil

def toolset(args):

    # Check if this is a new setip
    if "toolsets" not in CONFIGURATION:
        print("New setup detected, setting toolsets in configuration", warning=True)
        CONFIGURATION["toolsets"] = {}
        json.dump(CONFIGURATION, open(CONFIG_PATH, "r+"), indent=4)

    if args.list:

        if len(CONFIGURATION["toolsets"]) == 0:
            print_("* No toolsets were added.")
            os._exit(0)

        table = PrintTable("", "tools")
        for tool_name, tools in CONFIGURATION["toolsets"].items():
            table.add(tool_name, "\n".join(tools))
        table.display()
        print_(f" {format_bold("*", ok=True)} Total: {len(CONFIGURATION['toolsets'])}")
        os._exit(0)

    # Add a new toolset if not existed
    if args.toolset not in CONFIGURATION["toolsets"]:
        if not args.new:
            print(
                f'toolset : Unable to find toolset with the name of "{args.toolset}". To create a new toolset, include the "-n" flag',
                error=True,
            )
            os._exit(1)

        CONFIGURATION["toolsets"][args.toolset] = []
        json.dump(CONFIGURATION, open(CONFIG_PATH, "r+"), indent=4)
        print(f'Successfully created new toolset "{args.toolset}"', ok=True)

    # Delete the toolset
    if args.remove:
        # Remove the toolset
        del CONFIGURATION["toolsets"][args.toolset]
        json.dump(CONFIGURATION, open(CONFIG_PATH, "w"), indent=4)
        print(f'Successfully deleted toolset "{args.toolset}"', ok=True)
        os._exit(0)

    # Add new tools
    if args.add:

        # Checking if the command exist
        for cmd in args.add.split(","):

            # Looping through each command
            cmd = cmd.strip()

            if shutil.which(cmd)==None:
                # Making sure the command exist
                print(f'add : Unable to locate "{cmd}" command. Skipped', error=True)
                continue

            CONFIGURATION["toolsets"][args.toolset] = list(set([*CONFIGURATION["toolsets"][args.toolset], cmd]))
            json.dump(CONFIGURATION, open(CONFIG_PATH, "w"), indent=4)
            print(f"add : Successfully added new tool \"{cmd}\"", ok=True)

        os._exit(0)

    # print(constant.CONFIGURATION)
    # print(args.toolset)
