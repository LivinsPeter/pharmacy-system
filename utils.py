from rich.prompt import Prompt
from db_config import create_connection

def press_enter_to_continue():
    """Pauses execution until the user presses Enter."""
    Prompt.ask("[italic]Press Enter to continue...[/italic]")

def get_next_id(table_name, prefix):
    """Generates the next ID for a given table and prefix."""
    conn = create_connection()
    if conn is None:
        return f"{prefix}001"
    cursor = conn.cursor()
    try:
        id_column = table_name[:-1] + "_id"
        cursor.execute(f"SELECT {id_column} FROM {table_name} ORDER BY {id_column} DESC LIMIT 1")
        last_id = cursor.fetchone()
        if last_id:
            last_num = int(last_id[0][len(prefix):])
            return f"{prefix}{last_num + 1:03d}"
        else:
            return f"{prefix}001"
    except Exception as e:
        print(f"Error generating next ID: {e}")
        return f"{prefix}001"
    finally:
        cursor.close()
        conn.close()