package main

import (
	"flag"
	"hack/coreutil"
	"hack/lib"
)

func wrapper(v flag.Value, f func(v flag.Value)) {
	f(v)
	defer lib.Wg.Done()
}

// Mapping string to an actual function
var Features map[string]func(v flag.Value) = map[string]func(v flag.Value){
	"start": func(v flag.Value) { wrapper(v, coreutil.Start) },
	"htb":   func(v flag.Value) { wrapper(v, coreutil.Htb) },
}
