package lib

import (
	"errors"
	"fmt"
	"log"
	"os"
	"os/exec"
)

func IsCommandExist(command string) bool {

	_, err := exec.LookPath(command)

	if err != nil {
		return false
	}

	return true
}

func IsHTBTokenSet() bool {

	return false
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
		printError(" Fatal : " + err.Error())
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

func printError(msg string) {
	fmt.Println("[" + BOLD + Red + "ERROR" + Reset + "]:" + msg)
}

func printOk(msg string) {
	fmt.Println("[" + BOLD + Green + "OK" + Reset + "]:" + msg)
}
