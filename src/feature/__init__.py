from argparse import ArgumentParser
from . import hackthebox
from . import smarttools

Services = {
    "htb": {
        "cmd": hackthebox.htb_service,
        "args": {
            "choices": ["on", "off", "enable", "disable"],
            "help": "turn on or off HackTheBox service",
        },
    },
    "box": {
        "cmd": hackthebox.hackthebox_boxes,
        "args": {
            "help": "Handle box-specific actions ( spawn/terminate/submit flag )",
        },
    },
    "toolset": {
        "cmd": smarttools.toolset,
        "args": {
            "help": "provide easy management on custom toolset",
            "nargs": "?",
            "const": "",
        },
    },
}
Optional_Args = (
    (["--noreg"], {"help": "ignore region switching", "action": "store_true"}),
    (["--stop"], {"help": "indicate stopping something", "action": "store_true"}),
    (["--submit"], {"help": "append to the -box argument to submit flag"}),
    (
        ["--list", "-l"],
        {
            "help": "list out specific units based on another command",
            "action": "store_true",
        },
    ),
    (
        ["--open", "-o"],
        {
            "help": "Open a list out specific units based on another command",
            "action": "store_true",
        },
    ),
    (
        ["--remove", "-r"],
        {
            "help": "remove a specific units based on another command",
            "action": "store_true",
        },
    ),
    (
        ["--add", "-a"],
        {
            "help": "Add a specific units based on another command",
        },
    ),
    (
        ["--delete", "-d"],
        {
            "help": "Delete a specific units based on another command",
        },
    ),
    (
        ["--start", "-s"],
        {
            "action": "store_true",
            "help": "Start a specific toolset",
        },
    ),
    (
        ["--new", "-n"],
        {
            "help": 'mark a unit as "new" based on another command',
            "action": "store_true",
        },
    ),
)


# Auto-format arguments
def set_and_parse_arguments(parser: ArgumentParser) -> None:

    # Add a mutually required group of arguments
    required_group = parser.add_mutually_exclusive_group(required=True)
    for arg, props in Services.items():
        required_group.add_argument(f"-{arg}", **props["args"])

    # Optional arguments
    for arg, props in Optional_Args:
        parser.add_argument(*arg, **props)

    # Start parsing
    return parser.parse_args()
