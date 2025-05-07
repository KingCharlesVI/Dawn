import json
import importlib.resources
import os
import subprocess
import urllib.request
import shutil
from pathlib import Path


def check_chocolatey():
    """Check if Chocolatey is installed."""
    try:
        subprocess.run(["choco", "--version"], check=True, stdout=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def install_chocolatey():
    """Install Chocolatey if it's not installed."""
    if not check_chocolatey():
        print("[yellow]Chocolatey is not installed. Installing Chocolatey...[/yellow]")
        try:
            # Install Chocolatey using PowerShell
            subprocess.run(
                ["powershell", "-Command", "Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"],
                check=True
            )
            print("[green]Chocolatey installed successfully![/green]")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install Chocolatey: {e}")


def list_presets():
    try:
        # Access the resources bundled inside the executable
        files = importlib.resources.files("dawn.presets").iterdir()
        return [p.name.replace(".json", "") for p in files if p.suffix == ".json"]
    except Exception as e:
        raise RuntimeError(f"Failed to list presets: {e}")


def load_builtin_preset(name: str):
    try:
        filename = name if name.endswith(".json") else f"{name}.json"
        # Open the resource from the bundled presets
        with importlib.resources.files("dawn.presets").joinpath(filename).open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Preset '{name}' not found")
    except Exception as e:
        raise RuntimeError(f"Failed to load preset: {e}")


def get_preset_summary(preset: dict):
    return {
        "Name": preset.get("name", "Unnamed"),
        "Version": preset.get("version", "N/A"),
        "Apps": preset.get("apps", []),
        "Custom Apps": [a.get("name", "Unnamed") for a in preset.get("custom_apps", [])]
    }


def fetch_installer(url: str, download_path: str):
    """Download installer from URL."""
    try:
        urllib.request.urlretrieve(url, download_path)
        return download_path
    except Exception as e:
        raise RuntimeError(f"Failed to download installer: {e}")


def install_program(installer_path: str, silent_args: str = '/silent'):
    """Install the program using the installer."""
    try:
        subprocess.run([installer_path, silent_args], check=True)
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Installation failed: {e}")


def is_program_installed(program_name: str) -> bool:
    """Check if a program is installed (for example by checking registry or specific files)."""
    # Example: Check if a program is in the "Program Files" directory
    program_path = Path(f"C:/Program Files/{program_name}")
    return program_path.exists()


def get_installer_url(app_name: str) -> str:
    """Map app name to its installer URL."""
    installer_map = {
        "chrome": "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
        "opera": "https://www.opera.com/computer/thanks?ni=stable&os=windows",
        "firefox": "https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-GB",
        "vscode": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user",
        "spotify": "https://download.scdn.co/SpotifySetup.exe",
        "github": "https://central.github.com/deployments/desktop/desktop/latest/win32",
        "discord": "https://discord.com/api/download?platform=win",
        "steam": "https://steamcdn-a.akamaihd.net/client/installer/SteamSetup.exe",
        "7zip": "https://sourceforge.net/projects/sevenzip/files/latest/download",
        "roblox": "https://www.roblox.com/download/client?os=win",
        "nzxt": "https://nzxt-app.nzxt.com/NZXT-CAM-Setup.exe",
        # Add more apps and URLs here
    }
    
    return installer_map.get(app_name, "")


def install_from_preset(preset: dict):
    """Install all apps from a given preset."""
    # Ensure Chocolatey is installed first
    if not check_chocolatey():
        install_chocolatey()

    for app_name in preset.get("apps", []):
        # Check if app is installed
        if not is_program_installed(app_name):
            # If the app is in Chocolatey, use Chocolatey to install
            if app_name in get_chocolatey_apps():
                install_with_chocolatey(app_name)
            else:
                # Otherwise, fallback to the normal installer
                installer_url = get_installer_url(app_name)  # You need to map app_name to installer URLs
                installer_path = fetch_installer(installer_url, f"{app_name}_installer.exe")
                if install_program(installer_path):
                    print(f"[green]✔️ Successfully installed {app_name}[/green]")
                else:
                    print(f"[red]❌ Failed to install {app_name}[/red]")
        else:
            print(f"[yellow]⚡ {app_name} is already installed[/yellow]")


def install_with_chocolatey(package_name: str):
    """Install a program using Chocolatey."""
    try:
        subprocess.run(["choco", "install", package_name, "-y"], check=True)
        print(f"[green]✔️ {package_name} installed successfully using Chocolatey.[/green]")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to install {package_name} with Chocolatey: {e}")


def get_chocolatey_apps():
    """Return a list of available Chocolatey package names for known apps."""
    return [
        "googlechrome",
        "opera",
        "qbittorrent",
        "discord",
        "steam",
        "firefox",
        "vscode",
        "7zip",
        "cdburnerxp",
        "ccleaner",
        "notepadplusplus",
        "git",
        "vlc",
        "audacity",
        "handbrake",
        "gimp",
        "blender",
        "libreoffice-fresh",
        "java",
        "python",
        "python3",
        "nodejs",
        "mongodb",
        "docker-desktop",
        "adobereader",
        "microsoft-teams",
        "slack",
        "zoom",
        "teamviewer",
        "postman",
        "intellijidea",
        "nginx",
        "mongodb",
        "kotlin",
        "ruby",
        "aws-cli",
        "azure-cli",
        "icue",
        "lghub",
        "adobereader",
    ]