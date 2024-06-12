package lib

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

const (
	userprofile_api string = "https://labs.hackthebox.com/api/v4/user/profile/basic/%d"
	userinfo_api    string = "https://www.hackthebox.com/api/v4/user/info"
	switchvpn_api   string = "https://labs.hackthebox.com/api/v4/connections/servers/switch/%d" // with an <ID> at the last part of the string
	getvpn_api      string = "https://labs.hackthebox.com/api/v4/access/ovpnfile/%d/0"          // Get the ovpn file here
)

// Global struct type for responses of the HTB API
type UserInfoResponse struct {
	Info struct {
		Id       int    `json:"id"`
		Name     string `json:"name"`
		Email    string `json:"email"`
		IsVip    bool   `json:"isVip"`
		ServerId int    `json:"server_id"`
		Avatar   string `json:"avatar"`
		Team     struct {
			Id     int    `json:"id"`
			Name   string `json:"name"`
			Avatar string `json:"avatar_thumb_url"`
		}
	}
}

// Global struct type for responses of HTB Profile
type UserProfileResponse struct {
	Profile struct {
		Id      int    `json:"id"`
		Name    string `json:"name"`
		Systems int    `json:"system_owns`
		Users   int    `json:"user_owns"`
		Team    struct {
			Id      int    `json:"id"`
			Name    string `json:"name"`
			Ranking int    `json:"ranking"`
			Avatar  string `json:"avatar_thumb_url"`
		}
		Respects int    `json:"respects"`
		Rank     string `json:"rank"`
		Avatar   string `json:"avatar"`
		IsVip    bool   `json:"isVip"`
		Country  string `json:"country_name"`
		Server   string `json:"server"`
	}
}

// All regions in HackTheBox
type Regiontype struct {
	code    string
	real_id int
}

var AllRegions map[int]Regiontype = map[int]Regiontype{
	1: {code: "EU Free 1", real_id: 1},
	2: {code: "EU Free 2", real_id: 201},
	3: {code: "EU Free 3", real_id: 253},
	4: {code: "US Free 1", real_id: 113},
	5: {code: "US Free 2", real_id: 202},
	6: {code: "US Free 3", real_id: 254},
	7: {code: "AU Free 1", real_id: 177},
	8: {code: "SG Free 1", real_id: 251},
}

// GLobal struct for the response of the Switching Region process
type SwitchRegionResponse struct {
	Status  bool   `json:"status"`
	Message string `json:"message"`
	Data    struct {
		Id              int    `json:"id"`
		Friendly_Name   string `json:"friendly_name"`
		Current_clients int    `json:"current_clients"`
		Location        string `json:"location"`
	}
}

func is_valid_json_response(resp *http.Response) error {
	status := strings.TrimSpace(resp.Header.Get("Content-Type")) // Succeed if return JSON
	if status != "application/json" && status != "text/plain; charset=UTF-8" {
		return errors.New(" invalid token")
	}
	return nil
}

func IsVPNfileExist() bool {
	return IsFileExist(HTB_PATH_OVPN)
}

func SwitchRegionVPN(region Regiontype) error {
	req, _ := http.NewRequest("POST", fmt.Sprintf(switchvpn_api, region.real_id), nil)
	req.Header.Add("Authorization", "Bearer "+strings.TrimSpace(Configuration.Token))

	// Switching region first
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if e := is_valid_json_response(resp); e != nil {
		return e
	}

	var regionresp SwitchRegionResponse
	body, err := io.ReadAll(resp.Body)
	json.Unmarshal(body, &regionresp)

	// Print out information on this
	PrintOk("successfully switched to " + region.code)
	PrintColorBold("	+ Fullname: ", Green)
	fmt.Println(regionresp.Data.Friendly_Name)
	PrintColorBold("	+ Clients : ", Green)
	fmt.Println(regionresp.Data.Current_clients)

	// Success
	return nil
}

func AskRegion() Regiontype {
	// Ask which region you wish to download the VPN in
	fmt.Println("===== Please select a region =====")
	fmt.Println(" 1. EU-1	2. EU-2")
	fmt.Println(" 3. EU-3	4. US-1")
	fmt.Println(" 5. US-2	6. US-3")
	fmt.Println(" 7. AU-1	8. SG-1")
	fmt.Println("==================================")

	var region int

	fmt.Print("[")
	PrintColorBold("region", Cyan)
	fmt.Print("] >> ")
	fmt.Scan(&region)

	return AllRegions[region]
}

func FetchOpenVPNData() error {

	// Fetching the API file
	PrintWarning("no openvpn file found")

	// pick a value pair
	var region Regiontype
	if !DISABLE_REGION_SELECT {

		// Asking for region
		region = AskRegion()

		// Switching
		SwitchRegionVPN(region)

	} else {
		region = AllRegions[Configuration.Default_region]
		PrintInfo("using default region => " + region.code)

		if region.code == CacheProfile.Profile.Server {
			// Same region, skipping
			fmt.Println(" => region unchanged. Skipped reconnection")
		} else {
			fmt.Println(" => new region detected, switching.")
			SwitchRegionVPN(region)

			// Saving back new cache
			CacheProfile.Profile.Server = region.code
			Save_to_Cache()
		}
	}

	req_vpn, _ := http.NewRequest("GET", fmt.Sprintf(getvpn_api, region.real_id), nil)
	req_vpn.Header.Add("Authorization", "Bearer "+strings.TrimSpace(Configuration.Token))
	// Downloading the openvpn file
	client := &http.Client{}
	resp_vpn, err_vpn := client.Do(req_vpn)
	if err_vpn != nil {
		return err_vpn
	}
	defer resp_vpn.Body.Close()
	if e := is_valid_json_response(resp_vpn); e != nil {
		return e
	}

	// Reading the VPN content
	content, err := io.ReadAll(resp_vpn.Body)
	if err != nil {
		return err
	}

	// Writing to disk
	err_ := os.WriteFile(HTB_PATH_OVPN, content, 0644)
	if err_ != nil {
		return err_
	}

	return nil
}

func FetchProfileInfo(token string) (UserProfileResponse, error) {

	var jsondata UserInfoResponse
	var profile UserProfileResponse

	// fetching HackTheBox profile information
	req, err := http.NewRequest("GET", userinfo_api, nil)
	req.Header.Add("Authorization", "Bearer "+strings.TrimSpace(token))

	// Sending the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {

		return profile, err
	}
	defer resp.Body.Close()

	// Checking the status, if returns an application/json then it succeeds, otherwise it fails
	if err := is_valid_json_response(resp); err != nil {
		return profile, err
	}

	// Extracting the body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return profile, err
	}
	json.Unmarshal(body, &jsondata)

	// Making a request to retrieve the profile
	req_profile, _ := http.NewRequest("GET", fmt.Sprintf(userprofile_api, jsondata.Info.Id), nil)
	req_profile.Header.Add("Authorization", "Bearer "+strings.TrimSpace(token))
	resp_profile, err_ := client.Do(req_profile)
	if err_ != nil {
		return profile, err
	}
	defer resp_profile.Body.Close()

	// Checing if the resp successe
	fmt.Println(resp_profile.Header.Get("Content-Type"))
	if err_ := is_valid_json_response(resp_profile); err_ != nil {
		return profile, err_
	}
	PrintOk(" token is valid")

	content, err := io.ReadAll(resp_profile.Body)
	if err != nil {
		return profile, err
	}
	json.Unmarshal(content, &profile)

	// caching
	e := os.WriteFile(HTB_PATH_CACHE, content, 0644)
	if e != nil {
		return profile, e
	}

	return profile, nil
}
