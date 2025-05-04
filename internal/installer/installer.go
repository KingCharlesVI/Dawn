package installer

import (
	"dawn/internal/preset"
	"fmt"
	"os/exec"
)

var silentArgs = map[string]string{
	"chrome":  "--silent --do-not-launch-chrome",
	"discord": "/S",
	"spotify": "/S",
	"steam":   "/S",
	"github":  "/S",
}

var downloadLinks = map[string]string{
	"chrome":  "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
	"discord": "https://discord.com/api/download?platform=win",
	"spotify": "https://download.scdn.co/SpotifySetup.exe",
	"steam":   "https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe",
	"github":  "https://central.github.com/deployments/desktop/desktop/latest/win32",
}

func Install(p preset.Preset) {
	for _, app := range p.Apps {
		url := downloadLinks[app]
		arg := silentArgs[app]
		runInstaller(app, url, arg)
	}
	for _, custom := range p.CustomApps {
		runInstaller(custom.Name, custom.URL, "/S")
	}
}

func runInstaller(name, url, args string) {
	fmt.Printf("Installing %s...\n", name)
	cmd := exec.Command("powershell", "Invoke-WebRequest", url, "-OutFile", name+".exe")
	cmd.Run()
	exec.Command(name+".exe", args).Run()
}
