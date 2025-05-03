package installer

import (
	"dawn/utils"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
)

type CustomApp struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type Preset struct {
	Name       string      `json:"name"`
	Version    string      `json:"version"`
	Apps       []string    `json:"apps"`
	CustomApps []CustomApp `json:"custom_apps,omitempty"`
}

func runInstaller(cmd string) {
	fmt.Println("Running:", cmd)
	exec.Command("cmd", "/C", cmd).Run()
}

func InstallFromPreset(filename string) {
	path := "presets/" + filename + ".json"
	data, err := ioutil.ReadFile(path)
	if err != nil {
		fmt.Println("Error reading preset file:", err)
		return
	}

	var preset Preset
	if err := json.Unmarshal(data, &preset); err != nil {
		fmt.Println("Invalid preset format:", err)
		return
	}

	fmt.Printf("Installing preset: %s (v%s)\n", preset.Name, preset.Version)

	for _, app := range preset.Apps {
		if cmd, ok := AppInstallers[app]; ok {
			runInstaller(cmd)
		} else {
			fmt.Printf("Unknown app: %s\n", app)
		}
	}

	if len(preset.CustomApps) > 0 {
		for _, custom := range preset.CustomApps {
			fmt.Printf("Installing custom app: %s\n", custom.Name)
			runInstaller(custom.URL)
		}
	}
}

func InstallFromURL(url string) {
	tempFile := "temp_preset.json"
	err := utils.DownloadFile(tempFile, url)
	if err != nil {
		fmt.Println("Failed to download preset:", err)
		return
	}
	defer os.Remove(tempFile)

	data, _ := ioutil.ReadFile(tempFile)
	var preset Preset
	json.Unmarshal(data, &preset)

	fmt.Printf("Installing remote preset: %s (v%s)\n", preset.Name, preset.Version)

	for _, app := range preset.Apps {
		if cmd, ok := AppInstallers[app]; ok {
			runInstaller(cmd)
		} else {
			fmt.Printf("Unknown app: %s\n", app)
		}
	}

	if len(preset.CustomApps) > 0 {
		for _, custom := range preset.CustomApps {
			fmt.Printf("Installing custom app: %s\n", custom.Name)
			runInstaller(custom.URL)
		}
	}
}
