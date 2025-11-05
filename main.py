
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

import admin_ui
import client_ui

console = Console()

import sys

def main_menu():
    console.clear()
    while True:
        console.print(Panel.fit(
            """[bold cyan]1.[/bold cyan] Admin Login
[bold cyan]2.[/bold cyan] Client Login
[bold cyan]3.[/bold cyan] Register as New Client
[bold red]4.[/bold red] Exit""",
            title="Main Menu"
        ))

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], default="4")

        if choice == "1":
            admin_ui.admin_login()
        elif choice == "2":
            client_ui.client_login()
        elif choice == "3":
            client_ui.register_client()
        elif choice == "4":
            console.print("Exiting...", style="bold red")
            break

if __name__ == "__main__":
    main_menu()
