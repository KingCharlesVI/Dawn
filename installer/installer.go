package installer

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os/exec"
)

func runInstaller(cmd string) {
	fmt.Println("Installing:", cmd)
	exec.Command("cmd", "/C", cmd).Run()
}

func InstallFromPreset(name string) {
	data, _ := ioutil.ReadFile("presets/default.json")
	var presets map[string][]string
	json.Unmarshal(data, &presets)

	apps, ok := presets[name]
	if !ok {
		fmt.Println("Preset not found.")
		return
	}

	for _, app := range apps {
		if cmd, ok := AppInstallers[app]; ok {
			runInstaller(cmd)
		}
	}
}

func InstallFromURL(url string) {
	// Placeholder: fetch JSON from URL and install
	fmt.Println("Not yet implemented.")
}

func InteractiveInstall() {
	fmt.Println("Interactive mode not implemented yet.")
}
