# Dawn

A CLI tool written in Go which can install multiple programs on a user's Windows machine. Essentially it is a CLI version of Ninite. By default the CLI will ship with several presets containing combinations of programs (including Discord, Steam, Chrome, Github, Spotify etc.).

## Commands

For interactive mode: dawn

With specific preset: dawn --preset [preset-name]

With custom preset url: dawn --url https://example.com/mypreset.json

## Important notes

1. The application requires administrator privileges to install software. If not run as admin, it will attempt to elevate privileges.
2. All installations are performed silently with appropriate command-line arguments.


## Potential Enhancements

1. Add command to list all available applications
2. Add command to list all available presets
3. Create website for download and documentation
