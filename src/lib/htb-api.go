package lib

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
)

const (
	userinfo_api string = "https://www.hackthebox.com/api/v4/user/info"
)

// Global struct type for responses of the HTB API
type UserInfoResponse struct {
	Info struct {
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

// GLobal struct for the response of the Switching Region process
type SwitchRegionResponse struct {
	Status  bool   `json:"status"`
	Message string `json:"message"`
	Data    struct {
		Id              string `json:"id"`
		Friendly_Name   string `json:"friendly_name"`
		Current_clients string `json:"current_clients"`
		Location        string `json:"location"`
	}
}

func FetchOpenVPNData() {

	type regiontype struct {
		code    string
		real_id int
	}

	values := map[int]regiontype{
		1: {code: "EU-1", real_id: 1},
		2: {code: "EU-2", real_id: 201},
		3: {code: "EU-3", real_id: 253},
		4: {code: "US-1", real_id: 113},
		5: {code: "US-2", real_id: 202},
		6: {code: "US-3", real_id: 254},
		7: {code: "AU-1", real_id: 177},
		8: {code: "SG-1", real_id: 251},
	}

	// Fetching the API file

	log.Println("no openvpn file found\n")

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

	// pick a value pair
	_ = values[region]

	// Structure
	// {
	// 	"status": true,
	// 	"message": "VPN Server switched",
	// 	"data": {
	// 	  "id": 251,
	// 	  "friendly_name": "SG Free 1",
	// 	  "current_clients": 62,
	// 	  "location": "SG"
	// 	}
	//   }

}

func FetchProfileInfo(token string) (UserInfoResponse, error) {

	var jsondata UserInfoResponse

	// fetching HackTheBox profile information
	req, err := http.NewRequest("GET", userinfo_api, nil)

	// add token
	req.Header.Add("Authorization", "Bearer "+strings.TrimSpace(token))

	// Sending the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return jsondata, err
	}
	defer resp.Body.Close()

	// Checking the status, if returns an application/json then it succeeds, otherwise it fails
	status := resp.Header.Get("Content-Type")
	if strings.TrimSpace(status) != "application/json" {
		return jsondata, errors.New(" invalid token")
	}

	// Extracting the body
	PrintOk(" valid token, saved to app-data")
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return jsondata, err
	}

	json.Unmarshal(body, &jsondata)

	return jsondata, nil
}
