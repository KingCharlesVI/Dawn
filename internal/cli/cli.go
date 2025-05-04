package cli

import (
	"bufio"
	"fmt"
	"os"

	"dawn/internal/installer"
	"dawn/internal/preset"
)

func RunInteractive() {
	fmt.Println("Available presets:")
	files, _ := os.ReadDir("presets")
	for _, file := range files {
		fmt.Println(" -", file.Name())
	}
	fmt.Print("\nEnter preset name: ")
	reader := bufio.NewReader(os.Stdin)
	presetName, _ := reader.ReadString('\n')
	presetName = presetName[:len(presetName)-1]

	p := preset.LoadLocal(presetName)
	ConfirmAndInstall(p)
}

func ConfirmAndInstall(p preset.Preset) {
	fmt.Printf("You are about to install the following programs from preset: %s\n", p.Name)
	for _, app := range p.Apps {
		fmt.Println(" -", app)
	}
	for _, app := range p.CustomApps {
		fmt.Println(" -", app.Name, "(custom)")
	}
	fmt.Print("Proceed? (y/n): ")
	var input string
	fmt.Scanln(&input)
	if input == "y" {
		installer.Install(p)
	} else {
		fmt.Println("Aborted.")
	}
}
