package lib

import (
	"os/user"
	"sync"
)

// User information
var CurrentUser *user.User
var Uid int
var Gid int

// Command line arguments specific
var DISABLE_REGION_SELECT bool
var START_HTB_SERVICE bool

// Goroutine counter
var Wg sync.WaitGroup

// Directory variables
var EXE_DIR string  // Where the current executable stand at
var APP_DATA string // Where custom data of the users will be stored
var HOME_PATH string
var CONFIG_PATH string // Where the config.json stands at
var ETC_PATH string    // Where the etc folder which stores third-party drivers and exe at
var LOG_PATH string    // Where the logs will be stored

// specific services
var HTB_PATH string       // Path to store HackTheBox specific configuration
var HTB_PATH_OVPN string  // Path to the VPN file
var HTB_PATH_CACHE string // Path to the profile cache json file

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
	Token          string `json:"htbtoken"`
	Default_region int    `json:"default_region"`
}

var Configuration ConfigData
var CacheProfile UserProfileResponse
