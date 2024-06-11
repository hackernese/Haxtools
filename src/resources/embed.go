package resources

import _ "embed"

var (
	//go:embed config.json
	ConfigurationContent string
)
