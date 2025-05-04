package main

import (
	"fmt"
	"os"

	"dawn/internal/admin"
	"dawn/internal/cli"
	"dawn/internal/preset"
)

func main() {
	admin.CheckOrExit()

	args := os.Args[1:]

	switch {
	case len(args) == 0:
		cli.RunInteractive()
	case args[0] == "--preset" && len(args) > 1:
		p := preset.LoadLocal(args[1])
		cli.ConfirmAndInstall(p)
	case args[0] == "--url" && len(args) > 1:
		p := preset.LoadRemote(args[1])
		cli.ConfirmAndInstall(p)
	default:
		fmt.Println("Usage:")
		fmt.Println("  dawn                 (interactive mode)")
		fmt.Println("  dawn --preset name   (use local preset)")
		fmt.Println("  dawn --url URL       (use remote preset)")
	}
}
