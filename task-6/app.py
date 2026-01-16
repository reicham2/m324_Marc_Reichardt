from flask import Flask, render_template
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    max_retries = 5
    for attempt in range(max_retries):
        try:
            return mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'mysql'),
                user=os.getenv('MYSQL_USER', 'demo'),
                password=os.getenv('MYSQL_PASSWORD', 'demo'),
                database=os.getenv('MYSQL_DATABASE', 'demo'),
                port=3306
            )
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed, retrying in 2 seconds...")
                time.sleep(2)
            else:
                raise e

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        # Get data from each table
        table_data = {}
        for table in tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = [col[0] for col in cursor.fetchall()]
            
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            table_data[table] = {
                'columns': columns,
                'rows': rows
            }
        
        cursor.close()
        conn.close()
        
        return render_template('index.html', tables=table_data)
    except Exception as e:
        return f"<h1>Fehler beim Verbinden mit der Datenbank</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
