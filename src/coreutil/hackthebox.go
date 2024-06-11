package coreutil

import (
	"flag"
	"fmt"
	"hack/lib"
)

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

		lib.PrintColorBold("Username: ", lib.Green)
		fmt.Println(user.Info.Name)

		lib.PrintColorBold("Email: ", lib.Green)
		fmt.Println(user.Info.Email)

		lib.PrintColorBold("Avatar: ", lib.Green)
		fmt.Println(user.Info.Avatar)

		lib.PrintColorBold("Server ID: ", lib.Green)
		fmt.Println(user.Info.ServerId)

		lib.PrintColorBold("Team: ", lib.Green)
		fmt.Println(user.Info.Team.Name)

		lib.PrintColorBold("Is vip: ", lib.Green)
		if user.Info.IsVip {
			lib.PrintColorBold("yes", lib.Green)
		} else {
			lib.PrintColorBold("no", lib.Red)
		}
		fmt.Println()

		// Save and reconfigure config json
		lib.Configuration.Token = token
		lib.Save_to_Json()
		lib.Parse_Json()

		lib.PrintOk("successfully configured the token")
	}

	// Checking if the ovpn file has been downloaded
	// if !lib.IsFileExist(filepath.Join(lib.APP_DATA, "htb.ovpn")) {

	// 	// Download the VPN file

	// }

	if v.String() == "on" {
		// Turn on the VPN

		lib.PrintInfo("turning on the VPN")

	} else {
		// Turn off the VPN
		lib.PrintInfo("turning off  the VPN")

	}
}
