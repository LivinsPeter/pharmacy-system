from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.table import Table
import utils
import inventory_report
import process_pres
from db_config import create_connection

console = Console()

def admin_login():
    console.clear()
    console.print("[bold green]Admin Login[/bold green]")
    username = Prompt.ask("Username", default="admin")
    password = Prompt.ask("Password", password=True)

    if username == "admin" and password == "password":
        console.print("Login successful!", style="bold green")
        utils.press_enter_to_continue()
        admin_menu()
    else:
        console.print("Invalid credentials!", style="bold red")
        utils.press_enter_to_continue()

def admin_menu():
    while True:
        console.clear()
        console.print(Panel.fit(
            """[bold cyan]1.[/bold cyan] Add Medicine
[bold cyan]2.[/bold cyan] Update/Delete Medicine
[bold cyan]3.[/bold cyan] View Inventory
[bold cyan]4.[/bold cyan] Process Prescriptions
[bold cyan]5.[/bold cyan] Generate Report
[bold red]6.[/bold red] Logout""",
            title="Admin Menu"
        ))

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"], default="6")

        if choice == "1":
            add_medicine()
        elif choice == "2":
            update_delete_medicine()
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            process_pres.process_prescriptions()
            utils.press_enter_to_continue()
        elif choice == "5":
            inventory_report.generate_inventory_report()
            utils.press_enter_to_continue()
        elif choice == "6":
            console.print("Logging out...", style="bold red")
            break

def add_medicine():
    console.clear()
    console.print("[bold green]Add New Medicine[/bold green]")
    medicine_id = utils.get_next_id('medicines', 'M')
    name = Prompt.ask("Medicine Name")
    category = Prompt.ask("Category")
    price = FloatPrompt.ask("Price")
    stock = IntPrompt.ask("Stock")
    expiry_date = Prompt.ask("Expiry Date (YYYY-MM-DD)")

    conn = create_connection()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO medicines VALUES (%s, %s, %s, %s, %s, %s)", (medicine_id, name, category, price, stock, expiry_date))
        conn.commit()
        console.print(f"Medicine [bold magenta]{name}[/bold magenta] added successfully with ID [bold yellow]{medicine_id}[/bold yellow]!", style="bold green")
    except Exception as e:
        conn.rollback()
        console.print(f"Database Error: {e}", style="bold red")
    finally:
        cursor.close()
        conn.close()
    utils.press_enter_to_continue()

def update_delete_medicine():
    console.clear()
    console.print("[bold yellow]Update/Delete Medicine[/bold yellow]")
    medicine_id = Prompt.ask("Enter Medicine ID to update/delete")

    conn = create_connection()
    if conn is None: return
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM medicines WHERE medicine_id = %s", (medicine_id,))
        medicine = cursor.fetchone()

        if not medicine:
            console.print(f"Error: Medicine ID '{medicine_id}' not found.", style="bold red")
            utils.press_enter_to_continue()
            return

        console.print("1. Update Medicine")
        console.print("2. Delete Medicine")
        choice = Prompt.ask("Choose an option", choices=["1", "2"], default="1")

        if choice == '1':
            console.print("Enter new details (leave blank to keep current value):")
            name = Prompt.ask(f"Name ({medicine['name']})") or medicine['name']
            category = Prompt.ask(f"Category ({medicine['category']})") or medicine['category']
            price = FloatPrompt.ask(f"Price ({medicine['price']})") or medicine['price']
            stock = IntPrompt.ask(f"Stock ({medicine['stock']})") or medicine['stock']
            expiry_date = Prompt.ask(f"Expiry Date ({medicine['expiry_date']})") or str(medicine['expiry_date'])

            cursor.execute("UPDATE medicines SET name=%s, category=%s, price=%s, stock=%s, expiry_date=%s WHERE medicine_id=%s", (name, category, price, stock, expiry_date, medicine_id))
            conn.commit()
            console.print("Medicine updated successfully!", style="bold green")
        elif choice == '2':
            cursor.execute("DELETE FROM orders WHERE medicine_id = %s", (medicine_id,))
            cursor.execute("DELETE FROM prescriptions WHERE medicine_id = %s", (medicine_id,))
            cursor.execute("DELETE FROM medicines WHERE medicine_id = %s", (medicine_id,))
            conn.commit()
            console.print("Medicine deleted successfully!", style="bold green")
    except Exception as e:
        conn.rollback()
        console.print(f"Database Error: {e}", style="bold red")
    finally:
        cursor.close()
        conn.close()
    utils.press_enter_to_continue()

def view_inventory():
    console.clear()
    conn = create_connection()
    if conn is None: return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM medicines")
        medicines = cursor.fetchall()
        table = Table(title="Inventory")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Category", style="green")
        table.add_column("Price", style="yellow")
        table.add_column("Stock", style="red")
        table.add_column("Expiry Date", style="blue")

        for med in medicines:
            table.add_row(med['medicine_id'], med['name'], med['category'], str(med['price']), str(med['stock']), str(med['expiry_date']))

        console.print(table)
    except Exception as e:
        console.print(f"Database Error: {e}", style="bold red")
    finally:
        cursor.close()
        conn.close()
    utils.press_enter_to_continue()