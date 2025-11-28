import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.db')
print(f"Testing connection to {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("SELECT successful")
    
    # Try a write operation (create a temp table)
    cursor.execute("CREATE TABLE IF NOT EXISTS _test_connection (id INTEGER PRIMARY KEY)")
    cursor.execute("INSERT INTO _test_connection DEFAULT VALUES")
    conn.commit()
    print("INSERT/COMMIT successful")
    
    cursor.execute("DROP TABLE _test_connection")
    conn.commit()
    print("DROP/COMMIT successful")
    
    conn.close()
    print("Connection closed successfully")
except Exception as e:
    print(f"Database error: {e}")
