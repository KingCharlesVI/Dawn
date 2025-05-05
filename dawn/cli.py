import argparse
import ctypes
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dawn import core
from dawn.version import __version__
from pathlib import Path

console = Console()

def check_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

def list_presets():
    try:
        presets = core.list_presets()
        console.print("[bold cyan]Available Built-in Presets:[/]")
        for p in presets:
            console.print(f"• {p}")
    except Exception as e:
        console.print(f"[red]❌ Failed to list presets: {e}[/red]")

def show_preset(source):
    try:
        if source.startswith("http://") or source.startswith("https://"):
            preset = core.load_external_preset(source)
        else:
            preset = core.load_builtin_preset(f"{source}.json")
        summary = core.get_preset_summary(preset)
        table = Table(title=f"{summary['Name']} (v{summary['Version']})")
        table.add_column("Type")
        table.add_column("Name")
        for app in summary["Apps"]:
            table.add_row("Built-in", app)
        for app in summary["Custom Apps"]:
            table.add_row("Custom", app)
        console.print(table)
    except FileNotFoundError:
        console.print(f"[red]❌ Preset '{source}' not found.[/red]")
    except Exception as e:
        console.print(f"[red]❌ Failed to load preset: {e}[/red]")

def confirm_install(preset):
    summary = core.get_preset_summary(preset)
    show_preset(summary["Name"])
    return console.input("[bold yellow]Proceed with install? (y/N): [/]").strip().lower() == 'y'

def install_from_preset(source):
    try:
        preset = core.load_builtin_preset(f"{source}.json")
        core.install_from_preset(preset)  # Install all apps in the preset
    except Exception as e:
        console.print(f"[red]❌ Failed to install preset: {e}[/red]")

def main():
    parser = argparse.ArgumentParser(prog="dawn", description="Batch install common apps on Windows.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available built-in presets")

    install_parser = subparsers.add_parser("install", help="Install from a preset name or URL")
    install_parser.add_argument("source", help="Preset name or URL")

    show_parser = subparsers.add_parser("show", help="Show contents of a preset by name or URL")
    show_parser.add_argument("source", help="Preset name or URL")

    subparsers.add_parser("version", help="Print Dawn version")

    args = parser.parse_args()

    if not check_admin():
        console.print(Panel("[red]❌ Dawn must be run as Administrator[/red]\nRight-click your terminal and 'Run as Administrator'"))
        return

    if args.command == "list":
        list_presets()
    elif args.command == "show":
        show_preset(args.source)
    elif args.command == "install":
        try:
            if args.source.startswith("http://") or args.source.startswith("https://"):
                preset = core.load_external_preset(args.source)
            else:
                preset = core.load_builtin_preset(f"{args.source}.json")
        except Exception as e:
            console.print(f"[red]❌ Failed to load preset: {e}[/red]")
            return

        if not confirm_install(preset):
            console.print("[red]Installation cancelled.[/red]")
            return

        # TODO: Implement actual install logic
        console.print("[green]✔️ Starting installation... (not implemented yet)[/green]")

    elif args.command == "version":
        console.print(f"Dawn version {__version__}")

if __name__ == "__main__":
    main()