package main

import (
	"dawn/installer"
	"dawn/utils"
	"flag"
	"fmt"
)

func main() {
	preset := flag.String("preset", "", "Install using a named preset (without extension)")
	url := flag.String("url", "", "Install using a remote preset URL")
	flag.Parse()

	utils.RequireAdmin()

	switch {
	case *preset != "":
		installer.InstallFromPreset(*preset)
	case *url != "":
		installer.InstallFromURL(*url)
	default:
		fmt.Println("No preset or URL provided. Usage: \ndawn --preset [name]\ndawn --url [url]")
	}
}
