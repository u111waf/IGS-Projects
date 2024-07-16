from app import mysql

def get_all_employees():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    cur.close()
    return employees

