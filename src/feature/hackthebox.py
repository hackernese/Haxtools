
"""
    References :
        1. https://github.com/D3vil0p3r/HackTheBox-API
        2. https://documenter.getpostman.com/view/13129365/TVeqbmeq#5cb306a0-9d1d-4b46-b9ca-eea2d105e8e9

    Commands:
        hack -box -l : List all active boxes
        hack --active-box : List active box
        hack -box <Name/ID> --start : Spawn a box
        hack -box <Name/ID> --stop : Stop a box
        hack -box <Name/ID> --submit=<flag> : Submit a flag

        hack -htb=on : Turning on hackthebox service
        hack -htb=off : Turning off hackthebox service
        hack -htb=enable : Enabling hackthebox service on start
"""

from constant import *
from typing import Optional
from logs import print, print_, Loading, format_bold
from urllib.parse import urlparse, parse_qs, ParseResultBytes
from utils import PrintTable
import http.client
import json
import pprint
import os
import subprocess
import sh


userprofile_api: str = "https://labs.hackthebox.com/api/v4/user/profile/basic/%d"
userinfo_api: str = "https://www.hackthebox.com/api/v4/user/info"
switchvpn_api: str = (
    "https://labs.hackthebox.com/api/v4/connections/servers/switch/%d"  # with an <ID> at the last part of the string
)
getvpn_api: str = (
    "https://labs.hackthebox.com/api/v4/access/ovpnfile/%d/0"  # Get the ovpn file here
)
active_machines : str = "https://labs.hackthebox.com/api/v4/machine/paginated?per_page=50" # GET
spawn_machine : str = "https://labs.hackthebox.com/api/v4/machine/play/%s" # POST
stop_active_machine : str = "https://labs.hackthebox.com/api/v4/machine/stop" # POST
submit_a_flag : str = "https://labs.hackthebox.com/api/v4/machine/own" # POST with JSON data -> Format : {"flag":"your-flag","id":480,"difficulty":50}
machine_info : str = "https://labs.hackthebox.com/api/v4/machine/profile/%s" # GET


def __request_with_token(
    url: str,
    method: str = "GET",
    token: str = None,
    success_type: str = "application/json",
    data : str = "",
    headers : dict = {}
) -> Optional[tuple[str | object,http.client.HTTPResponse]] | None:
    """Making a request to the HTB APIv4 with authorization token

    Returns:
        str : very likely to be an openvpn content
        object : a successfully parsed json object
        None : fail to make request, very likely due to invalid token
    """

    # Parsing the URL first
    parsedUrl: ParseResultBytes = urlparse(url)
    origin: str = parsedUrl.netloc
    path: str = parsedUrl.path

    # Making http connection
    conn: http.client.HTTPSConnection = http.client.HTTPSConnection(origin)
    conn.request(
        method,
        path,
        data,
        {"Authorization": f"Bearer {token if token else CONFIGURATION['htbtoken']}", **headers},
    )
    response: http.client.HTTPResponse = conn.getresponse()
    result: bytes = response.read()

    # Checking if it was valid
    if response.getheader("Content-Type") != success_type:
        return None, 'Invalid token, please recheck or generate a new one.' if response.getheader("Content-Type").startswith('text/html') else result.decode('utf-8')

    ret = result.decode("utf-8")
    return (ret if success_type == "text/plain; charset=UTF-8" else json.loads(ret), None)


def __check_htbtoken() -> bool:

    if "htbtoken" in CONFIGURATION and CONFIGURATION["htbtoken"].strip() != "":
        return True

    # Not configured
    token = None
    print("Missing HackTheBox token. Please provide one", warning=True)
    while not token:
        print_(f"[{format_bold("token", "info")}]", end="")
        token = input(">> ").strip()

    loader = Loading(" => Fetching information...")

    # Making sure the token is valid
    userinfo, error_resp = __request_with_token(userinfo_api, token=token)
    if userinfo == None:
        loader.stop(False)
        print("invalid token, authorization failed.", error=True)
        return False

    # Grabbing the profile information
    profile, error_resp = request_profile(userinfo["info"]["id"], token)

    if profile == None:
        loader.stop(False)
        print("Invalid token, authorization failed.", error=True)
        return False

    loader.stop(True)

    # Printing a pretty table
    PrintTable("Attr", "").add("ID", profile["profile"]["id"]).add(
        "Name", profile["profile"]["name"]
    ).add("Country", profile["profile"]["country_name"]).add(
        "VIP", profile["profile"]["isVip"]
    ).add(
        "Rank", profile["profile"]["rank"]
    ).add(
        "Server", profile["profile"]["server"]
    ).display()

    # Saving json back to the file
    CONFIGURATION["htbtoken"] = token
    json.dump(CONFIGURATION, open(CONFIG_PATH, "r+"), indent=4)
    print(f"Saved token to {CONFIG_PATH}", ok=True)

    return True


def switch_vpn() -> int | None:

    print("Switching region enabled", info=True)
    print_(" => Please select one of the following regions")

    # Printing region table
    table = PrintTable("ID", "Region")
    for i, reg in REGIONS.items():
        table.add(i,reg['name'])
    table.display()

    # region_obj will store the information about the region
    region_obj = None
    region_id = None

    # Assking for region ID
    while True:
        print_(f"[{format_bold("ID", "info")}]", end="")
        try:
            _ = int(input(">> ").strip())
            region_obj = REGIONS[_]
            region_id = _
            break
        except KeyboardInterrupt:
            print_("\n-- Abort --")
            os._exit(1)
        except:
            print("Invalid region, please try again.", error=True)

    # Sending request to switch
    print(f"Selected region \"{format_bold(region_obj['name'], "info")}\"", info=True)
    loader = Loading(f" => Switching to {region_obj['name']}")
    resp, error_resp = __request_with_token(switchvpn_api % region_id, method="POST")


    # checking if switching was successful
    if resp == None:
        loader.stop(False)
        print(f"Unable to switch to {region_obj['name']}", error=True)
        return False

    loader.stop(True)

    # return the region id on success
    return region_id

def download_vpn(region_id : int) -> bool:

    loader = Loading(f" => Downloading openvpn configuration [region=\"{REGIONS[region_id]['name']}\"]")
    resp, err_resp = __request_with_token(getvpn_api % region_id, success_type="text/plain; charset=UTF-8")

    # Checking for error
    if resp==None:
        loader.stop(False)
        print("Unable to download vpn configuration", error=True)
        return

    # Saving the file into disk
    with open(HTB_OVPN, "w") as proto:
        proto.write(resp)
    loader.stop(True)


request_profile = lambda id_ , token :__request_with_token(userprofile_api % id_, token=token)

def htb_service(args) -> None:

    # Make sure the token is already configured
    if not __check_htbtoken():
        return

    # Downloading the openvpn
    if not os.path.isfile(HTB_OVPN):

        print_()
        print("No openvpn file found. Configuring", warning=True)


        reg_id = CONFIGURATION["default_region"]

        # if the --noreg flag is not set
        if not args.noreg:
            reg_id = switch_vpn()
            if reg_id==None:
                raise Exception("region ID is None")
        else:
            print(f"Using default region \"{format_bold(REGIONS[reg_id]['name'], 'info')}\"", info=True)

        # Download and save the VPN configuration
        download_vpn(reg_id)

    # Check if there has already been a polkit rule and a systemd service being set
    service_exist = os.path.isfile(HTB_SERVICE_PATH)   # /etc/systemd/system

    try:
        if not service_exist:
            (print("No hackthebox service detected.", warning=True) if not service_exist else None)
            print("Root permission is required to setup missing configurations.", info=True)
            # Adding
            with sh.contrib.sudo:

                # Create a temporary service file to store the content
                open("/tmp/hackthebox.service.tmp", "w").write(HTB_SERVICE)
                sh.cp("/tmp/hackthebox.service.tmp", HTB_SERVICE_PATH)
                os.remove("/tmp/hackthebox.service.tmp")

                sh.cp(HTP_POLKIT_ASSET, HTB_POLKIT_PATH)

                # Restarting services
                sh.systemctl("daemon-reload")
                sh.systemctl("restart", "hackthebox", "polkit")
    except sh.ErrorReturnCode_1:
        print("Invalid password.", error=True)
        os._exit(2)

    # Starting the service
    try:

        l = None

        if args.htb=="on":
            l = Loading(" => Turning on HTB instance")
            sh.systemctl("start", "hackthebox")
            l.stop(True)
            print("HTB instance successfully started", ok=True)
        elif args.htb=="off":
            l = Loading(" => Turning off HTB instance")
            sh.systemctl("stop", "hackthebox")
            l.stop(True)
            print("HTB instance successfully terminated", ok=True)
        elif args.htb=="disable":
            l = Loading(" => Disabling HTB instance on startup")
            sh.systemctl("disable", "hackthebox")
            l.stop(True)
            print("HTB instance successfully disabled", ok=True)
        else:
            # Enabling the service
            l = Loading(" => Enabling HTB instance on startup")
            sh.systemctl("enable", "hackthebox")
            l.stop(True)
            print("HTB instance enabled", ok=True)
    except sh.ErrorReturnCode_1:
        l.stop(False)
        print("Invalid password", error=True)

def __list_box_or_fatal(loading_msg : str) -> dict:
    loader = Loading(f" * {loading_msg}")
    resp, error_msg = __request_with_token(active_machines, token=CONFIGURATION['htbtoken'])
    if resp==None:
        loader.stop(False)
        print(error_msg, error=True)
        os._exit(1)
    loader.stop(True)

    return resp


def __load_box_profile_info_or_fatal(name : str , no_loader=False) -> dict:
    if not no_loader:
        loader = Loading(f" * Requesting profile information of box \"{format_bold(name, 'info')}\"")

    resp, error_msg = __request_with_token(machine_info % name, token=CONFIGURATION['htbtoken'])
    if resp==None:
        loader.stop(False)
        print(error_msg, error=True)
        os._exit(1)

    if not no_loader:
        loader.stop(True)

    return resp

def hackthebox_boxes(args) -> None:


    # hack -box -l : List all active boxes
    # hack -box --active : List active box
    # hack -box <Name/ID> --start : Spawn a box
    # hack -box <Name/ID> --stop : Stop a box
    # hack -box <Name/ID> --submit=<flag> : Submit a flag

    # Make sure the token is already configured
    if not __check_htbtoken():
        return

    # Make sure that there are some arguments
    if args.box != "list" and args.box != "active" and not args.start and not args.stop and not args.submit:
        return

    # Get a bunch of active boxes
    loader = Loading(f" * Loading data about existing boxes")
    resp_json, error_msg = __request_with_token(active_machines, token=CONFIGURATION['htbtoken'])
    if resp_json==None:
        loader.stop(False)
        print(error_msg, error=True)
        os._exit(1)
    loader.stop(True)


    # List all boxes
    if args.box =="list":

        # Printing machines in beautiful tables
        table = PrintTable("ID", "Name", "Difficulty", "OS", "Seasonal", nobold=True)
        for record in resp_json['data']:
            color = "ok" if record['difficultyText'] == "Easy" else "error" if record['difficultyText']=="Hard" else "warning" if record['difficultyText']=="Medium" else "info"
            table.add( str(record["id"]),
                format_bold(
                    record['name'], color=color
                ), record['difficultyText'], record['os'],
                    "YES" if record['labels'] and record['labels'][0]['name']=="SEASONAL" else "No"
                )
        table.display()

        # Printing indicator color
        print_(f" * {format_bold('Total', 'ok')} : {len(resp_json['data'])} boxes")
        return

    # List the currently active box
    if args.box =="active":

        boxes_found = 0

        for box in resp_json['data']:
            if box['active']:
                # Loading profile information
                response = __load_box_profile_info_or_fatal(box['name'])

                print_(f" * Active box found : {format_bold(box['name'], "ok")}")
                print_(f" ├─ ID : {box['id']}")
                print_(f" ├─ IP : {response['info']['ip']}")
                print_(f" ├─ OS : {box['os']}")
                print_(f" └─ Difficulty : {box['difficultyText']}")
                boxes_found = boxes_found+1

        if boxes_found==0:
            print("No box is currently active", info=True)

        return

    # Check if -box is a number or a string
    box_json = None
    try:
        # -box value is an integer, possibly an ID
        box_id = int(args.box.strip())
        box = [box for box in resp_json['data'] if box['id'] == box_id]
        if not box:
            # NO Box found
            print(f"Unable to find a box with the ID of {box_id}", error=True)
            os._exit(1)

        box_json = box[0]
    except ValueError:
        box = [box for box in resp_json['data'] if box['name'] == args.box]
        if not box:
            # No box found
            print(f"Unable to find a box with the name of \"{args.box}\"", error=True)
            os._exit(1)

        # Found a box
        box_json = box[0]

    # Submit a flag
    if args.submit:
        loader = Loading(f" * Submiting flag = \"{format_bold(args.submit, 'info')}\"")

        # Make a http request
        resp_json, error_msg = __request_with_token(submit_a_flag, method="POST",
        data=json.dumps({
            "flag":args.submit.strip(),"id":box_json['id'],"difficulty":box_json['difficulty']
        }),
        headers={"Content-Type": "application/json"},
        token=CONFIGURATION['htbtoken'])

        # Error checking
        if resp_json==None:
            loader.stop(False)
            print(error_msg, error=True)
            os._exit(1)

        # Checking if the flag is correct
        status = resp_json['status'] != 400
        loader.stop(status)
        print(resp_json['message'],  **{'ok' if status else 'error' : True})
        return

    # Spawn a machine
    if args.start:
        loader = Loading(f" * Starting machine \"{format_bold(box_json['name'], 'info')}\"")

        # Make a http request
        resp_json, error_msg = __request_with_token(spawn_machine % box_json['id'], method="POST", token=CONFIGURATION['htbtoken'])

        # Error checking
        if resp_json==None:
            loader.stop(False)
            print(error_msg, error=True)
            os._exit(1)

        # Checking if the flag is correct
        loader.stop(resp_json['success'])

        # Loading profile information
        profile = __load_box_profile_info_or_fatal(box_json['name'])

        print(resp_json['message'],  **{'ok' if resp_json['success'] else 'error' : True})
        print_(f" └─ IP : {format_bold(profile['info']['ip'], 'ok')}")
        return

    # Stop a machine
    if args.stop:
        loader = Loading(f" * Stopping machine \"{format_bold(box_json['name'], 'info')}\"")

        # Make a http request
        resp_json, error_msg = __request_with_token(stop_active_machine, method="POST", token=CONFIGURATION['htbtoken'])

        # Error checking
        if resp_json==None:
            loader.stop(False)
            print(error_msg, error=True)
            os._exit(1)

        # Checking if the flag is correct
        loader.stop(True)
        print(resp_json['message'], ok=True)
        return
