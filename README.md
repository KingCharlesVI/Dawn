# Dawn

A CLI tool written in Go which can install multiple programs on a user's Windows machine. Essentially it is a CLI version of Ninite. By default the CLI will ship with several presets containing combinations of programs (including Discord, Steam, Chrome, Github, Spotify etc.). Custom presets can also be imported.

## Commands

For interactive mode: dawn

With specific preset: dawn --preset [preset-name]

With custom preset url: dawn --url https://example.com/mypreset.json

## Presets

Presets will be stored in separate .json files. Here is an example of a preset file called awesomepreset.json:

{
  "name": "Awesome Preset",
  "version": "1.0",
  "apps": ["chrome", "discord", "spotify"],
  "custom_apps": [
    {
      "name": "Internal Tool",
      "url": "https://example.com/internaltool/setup.exe"
    },
    {
      "name": "Proprietary VPN",
      "url": "https://vpn.example.com/vpn_installer.exe"
    }
  ]
}

The custom_apps is optional

## Workflow

The user should confirm the list of programs to be installed.

## Important notes

1. The application requires administrator privileges to install software. If not run as admin, it will attempt to elevate privileges.
2. All installations are performed silently with appropriate command-line arguments.


## Potential Enhancements

1. Add command to list all available applications
2. Add command to list all available presets
3. Create website for download and documentation
