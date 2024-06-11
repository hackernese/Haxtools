package coreutil

import (
	"flag"
)

func Htb(v flag.Value) {
	/*
		Starting hackthebox service ( VPN ) using HackTheBox APIv4
		Reference :
		+ https://github.com/D3vil0p3r/HackTheBox-API
		+ https://documenter.getpostman.com/view/13129365/TVeqbmeq#5cb306a0-9d1d-4b46-b9ca-eea2d105e8e9

		URL to VPN : https://labs.hackthebox.com/api/v4/access/ovpnfile/<ID>/0

		IDs :
			- 251 : Singapore

	*/

	if v.String() == "on" {
		// Turn on the VPN

	} else {
		// Turn off the VPN
	}
}
