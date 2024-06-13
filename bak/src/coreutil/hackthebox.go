package coreutil

import (
	"flag"
	"fmt"
	"hack/lib"
	"os/exec"
)

func aaa() bool {
	return true
}

var aa bool = aaa()

func Htb(v flag.Value) {
	/*
		Starting hackthebox service ( VPN ) using HackTheBox APIv4
		References :
		+ https://github.com/D3vil0p3r/HackTheBox-API
		+ https://documenter.getpostman.com/view/13129365/TVeqbmeq#5cb306a0-9d1d-4b46-b9ca-eea2d105e8e9

		URL to VPN : https://labs.hackthebox.com/api/v4/access/ovpnfile/<ID>/0

		IDs :
			- 251 : Singapore

	*/
	if !lib.IsHTBTokenSet() {
		lib.PrintWarning(" HackTheBox app token isn't configured.")
		lib.PrintInfo(" Get a token at https://app.hackthebox.com/profile/settings then click on \"CREATE APP TOKEN\"")
		fmt.Println("\n----Please provide your token----")

		var token string

		fmt.Print("[")
		lib.PrintColorBold("token", lib.Cyan)
		fmt.Print("] >> ")
		fmt.Scanln(&token)

		// Making sure the token is correct
		user, err := lib.FetchProfileInfo(token)
		if err != nil {
			lib.PrintError(err.Error())
			return
		}

		lib.PrintColorBold("	+ Username: ", lib.Green)
		fmt.Println(user.Profile.Name)

		lib.PrintColorBold("	+ Rank    : ", lib.Green)
		fmt.Println(user.Profile.Rank)

		lib.PrintColorBold("	+ Avatar  : ", lib.Green)
		fmt.Println(user.Profile.Avatar)

		lib.PrintColorBold("	+ Country : ", lib.Green)
		fmt.Println(user.Profile.Country)

		lib.PrintColorBold("	+ Team    : ", lib.Green)
		fmt.Println(user.Profile.Team.Name)

		lib.PrintColorBold("	+ VIP     : ", lib.Green)
		if user.Profile.IsVip {
			lib.PrintColorBold("yes", lib.Green)
		} else {
			lib.PrintColorBold("no", lib.Red)
		}

		lib.PrintColorBold("	+ Server  : ", lib.Green)
		fmt.Println(user.Profile.Server)

		fmt.Println()

		// Save and reconfigure config json
		lib.Configuration.Token = token
		lib.Save_to_Json()
		lib.Parse_Json()

		lib.PrintOk("successfully configured the token")
	}

	// Checking if the ovpn file has been downloaded
	if !lib.IsVPNfileExist() {
		// Download the VPN file
		if err := lib.FetchOpenVPNData(); err != nil {
			lib.PrintError(err.Error())
			return
		}
		lib.PrintOk(" successfully downloaded vpn configuration")
	}

	if v.String() == "on" {

		channel := lib.PrintLoadingBar(" => Starting HackTheBox service")

		// Turn on the VPN
		cmd := exec.Command("systemctl", "start", "hackthebox")
		_, err := cmd.Output()
		if err != nil {
			lib.EndPrintingLoadingBar(channel, false)
			lib.PrintError(err.Error())
			return
		}

		lib.EndPrintingLoadingBar(channel, true)

	} else {
		channel := lib.PrintLoadingBar(" => Stopping HackTheBox service")

		// Turn off the VPN
		cmd := exec.Command("systemctl", "stop", "hackthebox")
		_, err := cmd.Output()
		if err != nil {
			lib.EndPrintingLoadingBar(channel, false)
			lib.PrintError(err.Error())
			return
		}

		lib.EndPrintingLoadingBar(channel, true)

	}
}
