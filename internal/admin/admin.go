package admin

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
)

// IsElevated returns true if the program is running with admin rights
func IsElevated() bool {
	cmd := exec.Command("net", "session")
	cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
	err := cmd.Run()
	return err == nil
}

// CheckOrExit checks admin status and exits if not elevated
func CheckOrExit() {
	if !IsElevated() {
		fmt.Println("❌ Dawn requires administrator privileges to install software.")
		fmt.Println("➡ Please run this terminal as Administrator and try again.")
		os.Exit(1)
	}
}
