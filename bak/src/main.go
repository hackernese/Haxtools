/*

	Usage :
		hack -htb=on  # Turn on hackthebox service
		hack -htb=off # Turn off hackthebox service

		hack -start 			 # Start a combination of tools
		hack -list-service 		 # List all registered tools
		hack -register=burpsuite # Register burpsuite into the list

		hack -seclist # Displaying seclist
*/

package main

import (
	"flag"
	"fmt"
	"hack/lib"
	"log"
	"os"
	"os/user"
	"path/filepath"
	"strconv"
)

func parse_args() {

	// Defining flags
	// --- HackTheBox related
	flag.String("htb", "", "Turn on or off HackTheBox VPN")
	flag.BoolVar(&lib.DISABLE_REGION_SELECT, "noreg", false, "Disable region selecting when dealing with HackTheBox VPN")
	flag.BoolVar(&lib.START_HTB_SERVICE, "start", false, "Start a combination of tools")

	flag.Bool("list-service", false, "List all registered tools")
	flag.String("register", "", "Register a new tool into the combination")
	flag.Bool("seclist", false, "Start the seclist navigator")

	// Parsing the flags
	flag.Parse()

	// Checking if the user provides any flag
	var anyflag int = 0
	flag.Visit(func(f *flag.Flag) {
		anyflag++

		// Execute the function
		if call, ok := Features[f.Name]; ok {
			lib.Wg.Add(1) // Increment the counter
			call(f.Value)
		}
	})

	if anyflag == 0 {
		fmt.Println("Usage:\n------------------------------------------")
		flag.PrintDefaults()
		fmt.Println("------------------------------------------")
		os.Exit(1)
	}

}

func initialize() {

	// Getting the current user information ( since this will be run as root )
	var err error
	lib.CurrentUser, err = user.Current()
	if err != nil {
		log.Fatal(err)
	}
	lib.Gid, err = strconv.Atoi(lib.CurrentUser.Gid)
	if err != nil {
		log.Fatal(err)
	}
	lib.Uid, err = strconv.Atoi(lib.CurrentUser.Uid)
	if err != nil {
		log.Fatal(err)
	}

	// Getting the directory where the exe is standing
	ex, err := os.Executable()
	if err != nil {
		panic(err)
	}
	lib.EXE_DIR = filepath.Dir(ex)

	// Setting up home path
	dirname_, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
	}
	lib.HOME_PATH = dirname_

	//Setting app data
	lib.APP_DATA = filepath.Join(lib.HOME_PATH, ".hack")
	lib.MakeDirIfNotExist(lib.APP_DATA)

	// COnfiguring logging
	lib.ConfigureLogging()

	// Setting config file path
	lib.CONFIG_PATH = filepath.Join(lib.APP_DATA, "config.json")
	lib.Parse_Json()

	// Setting specific application paths
	lib.HTB_PATH = filepath.Join(lib.APP_DATA, "htb")
	lib.HTB_PATH_OVPN = filepath.Join(lib.HTB_PATH, "vpn.ovpn")
	lib.HTB_PATH_CACHE = filepath.Join(lib.HTB_PATH, "cache.json")
	lib.MakeDirIfNotExist(lib.HTB_PATH)
	lib.Parse_Cache_Profile() // Extract cached HackTheBox profile

}

func main() {

	// Initializing necessary variables
	initialize()

	// Parsing arguments first before proceeding
	parse_args()

	// Wait until all goroutines end before exitting
	lib.Wg.Wait()
}
