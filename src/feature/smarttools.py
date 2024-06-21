"""
    Commands:
        hack -toolset=<name> -o  : Open up a toolset

        hack -toolset=<name> -n : Provide the name of the toolset
        hack -toolset=<name> -r : Delete a specific toolset
        hack -toolset=<name> -l : List all existing toolset

        hack -toolset=<name> --add=<new command> : Register a new tool to easily startup
        hack -toolset=<name> --del=<new command> : Unregister a tool from the toolset
"""

from constant import *
from utils import *
from logs import *
from multiprocessing import Process
import os
import json
import pprint
import shutil
import subprocess
import constant

def __tool_child_process(tool):
    subprocess.call([tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def toolset(args):
    # Check if this is a new setip
    if "toolsets" not in CONFIGURATION:
        print("New setup detected, setting toolsets in configuration", warning=True)
        CONFIGURATION["toolsets"] = {}
        json.dump(CONFIGURATION, open(CONFIG_PATH, "r+"), indent=4)

    # Listing all toolsets ( -l )
    if args.list:

        if len(CONFIGURATION["toolsets"]) == 0:
            print_("* No toolsets were added.")
            os._exit(0)

        table = PrintTable("Name", "tools")
        for tool_name, tools in CONFIGURATION["toolsets"].items():
            table.add(tool_name, "\n".join(tools))
        table.display()
        print_(f" {format_bold("*", "ok")} Total: {len(CONFIGURATION['toolsets'])} set(s)")
        os._exit(0)

    if args.toolset == "":
        constant.GLOBAL_PARSER.print_help()
        os._exit(1)

    # Add a new toolset if not existed ( -n )
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

    # Start the toolset
    if args.open:
        for tool in CONFIGURATION["toolsets"][args.toolset]:
            Process(target=__tool_child_process, args=[tool]).start()
            print(f"Started \"{tool}\"", ok=True)
        os._exit(0)

    # Delete the toolset ( -r )
    if args.remove:
        # Remove the toolset
        del CONFIGURATION["toolsets"][args.toolset]
        json.dump(CONFIGURATION, open(CONFIG_PATH, "w"), indent=4)
        print(f'Successfully deleted toolset "{args.toolset}"', ok=True)
        os._exit(0)

    # Add new tools ( --add )
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

    # Delete a tool out of a set ( --del )
    if args.delete:

        tools = set(CONFIGURATION["toolsets"][args.toolset])

        # Checking if the command exist
        for cmd in args.delete.split(","):

            # Looping through each command
            tools.discard(cmd.strip())

            CONFIGURATION["toolsets"][args.toolset] = list(tools)
            json.dump(CONFIGURATION, open(CONFIG_PATH, "w"), indent=4)

        print(f"delete : Successfully removed specified tools from \"{args.toolset}\" toolset", ok=True)
        os._exit(0)
