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
    "toolset": {
        "cmd": smarttools.toolset,
        "args": {"help": "provide easy management on custom toolset"},
    },
}
Optional_Args = (
    (["--noreg"], {"help": "ignore region switching", "action": "store_true"}),
    (
        ["--list", "-l"],
        {
            "help": "list out specific units based on another command",
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
            "help": "Add a specific units based on another command",
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
