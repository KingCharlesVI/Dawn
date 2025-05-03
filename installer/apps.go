package installer

var AppInstallers = map[string]string{
	"chrome":  "https://dl.google.com/chrome/install/latest/chrome_installer.exe /silent /install",
	"discord": "https://discord.com/api/download?platform=win /S",
	"steam":   "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe /S",
	"spotify": "https://download.scdn.co/SpotifySetup.exe /silent",
	"github":  "https://central.github.com/deployments/desktop/desktop/latest/win /silent",
}
