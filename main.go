package main

import (
	"flag"

	"dawn/installer"
	"dawn/utils"
)

func main() {
	preset := flag.String("preset", "", "Install using a built-in preset")
	url := flag.String("url", "", "Install using a remote preset URL")
	flag.Parse()

	utils.RequireAdmin()

	switch {
	case *preset != "":
		installer.InstallFromPreset(*preset)
	case *url != "":
		installer.InstallFromURL(*url)
	default:
		installer.InteractiveInstall()
	}
}
