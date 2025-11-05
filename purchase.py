
from rich.console import Console
from db_config import create_connection

console = Console()

PRESCRIPTION_CATEGORIES = {'Analgesic', 'Antibiotic'}

def place_order(client_id, medicine_id, quantity):
    conn = create_connection()
    if conn is None: return "Error: Could not connect to the database."
    cursor = conn.cursor(dictionary=True)

    try:
        # Get Medicine Information
        cursor.execute("SELECT * FROM medicines WHERE medicine_id = %s", (medicine_id,))
        medicine = cursor.fetchone()

        if not medicine:
            return f"Error: Medicine ID '{medicine_id}' not found."

        med_name = medicine['name']
        category = medicine['category']
        current_stock = medicine['stock']

        # Prescription Check
        if category in PRESCRIPTION_CATEGORIES:
            console.print(f"Info: Medicine '{med_name}' requires a prescription.")
            cursor.execute("SELECT 1 FROM prescriptions WHERE client_id = %s AND medicine_id = %s AND status = 'Active' LIMIT 1", (client_id, medicine_id))
            if not cursor.fetchone():
                return f"Error: Order for '{med_name}' cannot be placed. Client '{client_id}' has no active prescription."
            console.print(f"Info: Active prescription found for client '{client_id}'.")

        # Stock Check
        if current_stock < quantity:
            return f"Error: Insufficient stock for '{med_name}'. Requested: {quantity}, Available: {current_stock}"

        console.print(f"Info: Stock check passed. Available: {current_stock}, Requested: {quantity}")

        # Place Order
        cursor.execute("SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1")
        last_id = cursor.fetchone()
        order_id = f"O{int(last_id['order_id'][1:]) + 1:03d}" if last_id else "O001"

        cursor.execute("INSERT INTO orders (order_id, client_id, medicine_id, qty, status) VALUES (%s, %s, %s, %s, 'Processing')", (order_id, client_id, medicine_id, quantity))
        cursor.execute("UPDATE medicines SET stock = stock - %s WHERE medicine_id = %s", (quantity, medicine_id))
        
        conn.commit()
        return f"Success: Order '{order_id}' placed for {quantity} x '{med_name}'. New stock: {current_stock - quantity}"

    except Exception as e:
        conn.rollback()
        return f"Database Error: {e}"
    finally:
        cursor.close()
        conn.close()
