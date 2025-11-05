
from db_config import create_connection

def cancel_order(order_id):
    conn = create_connection()
    if conn is None: return "Error: Could not connect to the database."
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()

        if not order:
            return f"Error: Order ID '{order_id}' not found."

        status = order['status']
        medicine_id = order['medicine_id']
        quantity_to_return = order['qty']

        if status in ('Shipped', 'Completed'):
            return f"Error: Order '{order_id}' cannot be cancelled. Status: {status}"
        
        if status == 'Cancelled':
            return f"Info: Order '{order_id}' is already cancelled."

        if status in ('Pending', 'Processing'):
            cursor.execute("UPDATE orders SET status = 'Cancelled' WHERE order_id = %s", (order_id,))
            cursor.execute("UPDATE medicines SET stock = stock + %s WHERE medicine_id = %s", (quantity_to_return, medicine_id))
            conn.commit()
            return f"Success: Order '{order_id}' has been cancelled. {quantity_to_return} unit(s) of '{medicine_id}' returned to stock."
        
        else:
            return f"Error: Unhandled order status '{status}'."

    except Exception as e:
        conn.rollback()
        return f"Database Error: {e}"
    finally:
        cursor.close()
        conn.close()
