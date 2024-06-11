package lib

import (
	"sync"
)

// Goroutine counter
var Wg sync.WaitGroup

// Directory variables
var EXE_DIR string  // Where the current executable stand at
var APP_DATA string // Where custom data of the users will be stored
var HOME_PATH string
var CONFIG_PATH string // Where the config.json stands at
var ETC_PATH string    // Where the etc folder which stores third-party drivers and exe at

// Exit code
const (
	JSON_ERROR        = -3
	UNSUPPORT_OS      = -1
	COMMAND_NOT_FOUND = -2
	UNEXPECTED_ERR    = 1
)

// Permissions
const (
	DIR_PERMISSION  = 0700 // Default to only the current user can read/write
	FILE_PERMISSION = 0700 // Same as above
)

// ANSI color codes
const (
	Reset   = "\033[0m"
	Red     = "\033[31m"
	Green   = "\033[32m"
	Yellow  = "\033[33m"
	Blue    = "\033[34m"
	Magenta = "\033[35m"
	Cyan    = "\033[36m"
	White   = "\033[37m"
)

// STYLING
const (
	RESET = "\033[0m"
	BOLD  = "\033[1m"
)

// Json types
type ConfigData struct {
	Seclisturl  string `json:"seclist_url"`
	Cheatsheets struct {
		All []string `json:"all"`
	}
	Token string `json:"htbtoken"`
}

var Configuration ConfigData
