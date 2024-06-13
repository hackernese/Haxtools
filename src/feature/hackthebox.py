"""
    References :
        1. https://github.com/D3vil0p3r/HackTheBox-API
        2. https://documenter.getpostman.com/view/13129365/TVeqbmeq#5cb306a0-9d1d-4b46-b9ca-eea2d105e8e9
"""

from constant import *
from typing import Optional
from logs import print, print_, Loading, format_bold
from urllib.parse import urlparse, parse_qs, ParseResultBytes
from utils import PrintTable
import http.client
import json
import pprint


userprofile_api: str = "https://labs.hackthebox.com/api/v4/user/profile/basic/%d"
userinfo_api: str = "https://www.hackthebox.com/api/v4/user/info"
switchvpn_api: str = (
    "https://labs.hackthebox.com/api/v4/connections/servers/switch/%d"  # with an <ID> at the last part of the string
)
getvpn_api: str = (
    "https://labs.hackthebox.com/api/v4/access/ovpnfile/%d/0"  # Get the ovpn file here
)


def __request_with_token(
    url: str,
    method: str = "GET",
    token: str = None,
    success_type: str = "application/json",
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
        "",
        {"Authorization": f"Bearer {token if token else CONFIGURATION['htbtoken']}"},
    )
    response: http.client.HTTPResponse = conn.getresponse()
    result: bytes = response.read()

    # Checking if it was valid
    if response.getheader("Content-Type") != success_type:
        return None, response

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

