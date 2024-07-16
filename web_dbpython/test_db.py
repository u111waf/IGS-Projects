from app import app, mysql

with app.app_context():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        print("Database connection successful")
        cur.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
