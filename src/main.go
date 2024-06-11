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
	"path/filepath"
)

func isFlagPassed(name string) bool {
	// Making sure a flag was provided
	found := false
	flag.Visit(func(f *flag.Flag) {

		// Found a flag, return true
		if f.Name == name {
			lib.Wg.Add(1)             // Increment the counter
			Features[f.Name](f.Value) // Call it concurrently

			found = true
		}
	})
	return found
}

func parse_args() {

	// Defining flags
	flag.String("htb", "", "Turning on or off HackTheBox VPN")
	flag.Bool("start", false, "Starting a combination of tools")
	flag.Bool("list-service", false, "List all registered tools")
	flag.String("register", "", "Register a new tool into the combination")
	flag.Bool("seclist", false, "Starting the seclist navigator")

	// Parsing the flags
	flag.Parse()

	// Checking if the user has provided any flag
	if !isFlagPassed("htb") && !isFlagPassed("start") && !isFlagPassed("list-service") &&
		!isFlagPassed("register") && !isFlagPassed("seclist") {
		fmt.Println("Usage:\n------------------------------------------")
		flag.PrintDefaults()
		fmt.Println("------------------------------------------")
		os.Exit(1)
	}
}

func initialize() {

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

	// Setting config file path
	lib.CONFIG_PATH = filepath.Join(lib.APP_DATA, "config.json")
	lib.Parse_Json()
}

func main() {

	// Initializing necessary variables
	initialize()

	// Parsing arguments first before proceeding
	parse_args()

	// Wait until all goroutines end before exitting
	lib.Wg.Wait()
}
