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

func PrintColorBold(msg string, color string) {
	fmt.Print(BOLD + color + msg + Reset)
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
