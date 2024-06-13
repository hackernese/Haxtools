package lib

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

var LogFile *os.File
var Writer *bufio.Writer

func PrintLoadingBar(text string) chan bool {

	channel := make(chan bool)
	var stop bool = false
	var status bool = false

	characters := []string{"⠋", "⠙", "⠴", "⠦"}

	go func() {
		defer close(channel)
		for !stop {

			for _, char := range characters {
				fmt.Print(text + " " + char + "\r")
				time.Sleep(200 * time.Millisecond)
			}

		}

		// Clear all on screen and append a [OK]
		if status {
			fmt.Println(text + fmt.Sprintf(" ✅"))
		} else {
			fmt.Println(text + fmt.Sprintf(" ❌"))
		}

		channel <- true
	}()

	go func() {
		status = <-channel
		stop = true
	}()

	return channel
}

func EndPrintingLoadingBar(channel chan bool, status bool) {
	channel <- status
	_ = <-channel
}

func ConfigureLogging() {
	LOG_PATH = filepath.Join(APP_DATA, "log")

	var err error

	// Create if not exist, and if it does, simply open it as READ + WRITE
	LogFile, err = os.OpenFile(LOG_PATH, os.O_RDWR|os.O_CREATE, 0644)
	if err != nil {
		log.Fatal("unable to configure logging")
	}

	// Create a writer
	Writer = bufio.NewWriter(LogFile)

}

func WriteToLog(content string) {
	_, err := Writer.WriteString(time.Now().UTC().Format("2006-01-02T15:04:05.999Z") + " " + content + "\n")
	if err != nil {
		fmt.Println("[Logging Error]: ", err)
		return
	}

	// Flush the buffered writer to ensure all data is written to the file
	err = Writer.Flush()
	if err != nil {
		fmt.Println("[Logging Error]: ", err)
		return
	}

}

func FormatColorBold(msg string, color string) string {
	return BOLD + color + msg + Reset
}

func PrintColorBold(msg string, color string) {
	fmt.Print(FormatColorBold(msg, color))
}

func PrintWarning(msg string) {
	content := ("[" + BOLD + Yellow + "WARNING" + Reset + "]:" + msg)
	WriteToLog(content)
	fmt.Println(content)
}

func PrintInfo(msg string) {
	content := ("[" + BOLD + Cyan + "INFO" + Reset + "]:" + msg)
	WriteToLog(content)
	fmt.Println(content)
}

func PrintError(msg string) {
	content := ("[" + BOLD + Red + "ERROR" + Reset + "]:" + msg)
	WriteToLog(content)
	fmt.Println(content)
}

func PrintOk(msg string) {
	content := ("[" + BOLD + Green + "OK" + Reset + "]:" + msg)
	WriteToLog(content)
	fmt.Println(content)
}
