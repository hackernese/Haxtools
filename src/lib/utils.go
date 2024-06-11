package lib

import (
	"encoding/json"
	"errors"
	"fmt"
	"hack/resources"
	"log"
	"os"
	"os/exec"
)

func Parse_Json() {
	if !IsFileExist(CONFIG_PATH) {

		// Create the config if it has not existed
		err := os.WriteFile(CONFIG_PATH, []byte(resources.ConfigurationContent), 0644)

		if err != nil {
			log.Fatal(err)
		}
	}

	// Parsing configuration file
	if content, err := os.ReadFile(CONFIG_PATH); err == nil {
		if err_ := json.Unmarshal([]byte(content), &Configuration); err_ != nil {
			log.Fatal(err_)
		}
	} else {
		log.Fatal(err)
	}
}

func Save_to_Json() {

	data, err := json.Marshal(Configuration)
	if err != nil {
		PrintError(err.Error())
	}

	err = os.WriteFile(CONFIG_PATH, data, 0644)
	if err != nil {
		PrintError(err.Error())
	}

}

func IsCommandExist(command string) bool {

	_, err := exec.LookPath(command)

	if err != nil {
		return false
	}

	return true
}

func IsHTBTokenSet() bool {
	return !(Configuration.Token == "")
}

func MakeDirOrFatal(dir string) bool {

	// Check if a directory has already existed first
	_, err := os.Stat(dir)

	if err == nil {

		// existed, skipping
		return true
	}

	// create a new directory
	err = os.Mkdir(dir, os.FileMode(DIR_PERMISSION))
	if err != nil {
		PrintError(" Fatal : " + err.Error())
		os.Exit(UNEXPECTED_ERR)
	}

	return false
}

func IsFileExist(path string) bool {
	if _, err := os.Stat(path); errors.Is(err, os.ErrNotExist) {
		return false
	}
	return true
}

func MakeDirIfNotExist(path string) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		err := os.Mkdir(path, 0700)
		if err != nil {
			log.Fatal(err)
		}
	}
}

func PrintColorBold(msg string, color string) {
	fmt.Print(BOLD + color + msg + Reset)
}

func PrintWarning(msg string) {
	fmt.Println("[" + BOLD + Yellow + "WARNING" + Reset + "]:" + msg)
}

func PrintInfo(msg string) {
	fmt.Println("[" + BOLD + Cyan + "INFO" + Reset + "]:" + msg)
}

func PrintError(msg string) {
	fmt.Println("[" + BOLD + Red + "ERROR" + Reset + "]:" + msg)
}

func PrintOk(msg string) {
	fmt.Println("[" + BOLD + Green + "OK" + Reset + "]:" + msg)
}
