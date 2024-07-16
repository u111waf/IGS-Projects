from flask import Flask, flash, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # password here
app.config['MYSQL_DB'] = 'employeedb'

mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST'])
def index():
    if request.method=='POST':
        EmployeeID = request.form['EmployeeID']
        Firstname = request.form['Firstname']
        Lastname = request.form['Lastname']
        Department = request.form['Department']
        Gender = request.form['Gender']
        Date = request.form['Date']

        if not (EmployeeID and Firstname and Lastname and Department and Gender and Date):
            flash('All fields are required!')
            return redirect(url_for('index'))


        cur = mysql.connection.cursor()
        try:
            cur.execute("""INSERT INTO employee (EmployeeID, Firstname, Lastname, Department, Gender, Date) VALUES (%s, %s, %s, %s, %s, %s)""",
            (EmployeeID, Firstname, Lastname, Department, Gender, Date))
            mysql.connection.commit()
            flash('Employee added successfully!')
        except Exception as e:
            flash(f'Error: {e}')
            mysql.connection.rollback()
        finally:
            cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    cur.close()

    return render_template('index.html', employees=employees)


     #   return 'Record Added Successfully'#redirect(url_for('index'))

    return render_template('index.html')

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee WHERE EmployeeID = %s", [id])
    employee = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        Firstname = request.form['Firstname']
        Lastname = request.form['Lastname']
        Department = request.form['Department']
        Gender = request.form['Gender']
        Date = request.form['Date']

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                UPDATE employee
                SET Firstname=%s, Lastname=%s, Department=%s, Gender=%s, Date=%s
                WHERE EmployeeID=%s
            """, (Firstname, Lastname, Department, Gender, Date, id))
            mysql.connection.commit()
            flash('Employee updated successfully!')
        except Exception as e:
            flash(f'Error: {e}')
            mysql.connection.rollback()
        finally:
            cur.close()

        return redirect(url_for('index'))

    return render_template('edit.html', employee=employee)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        EmployeeID = request.form['EmployeeID']
        Firstname = request.form['Firstname']
        Lastname = request.form['Lastname']
        Department = request.form['Department']
        Gender = request.form['Gender']
        Date = request.form['Date']

        if not (EmployeeID and Firstname and Lastname and Department and Gender and Date):
            flash('All fields are required!')
            return redirect(url_for('index'))

        cur = mysql.connection.cursor()       
        try:
            cur.execute("""
            UPDATE employee
            SET Firstname=%s, Lastname=%s, Department=%s, Gender=%s, Date=%s
            WHERE EmployeeID=%s
            """, (Firstname, Lastname, Department, Gender, Date, EmployeeID))
            mysql.connection.commit()
            flash('Record updated successfully!')
        except Exception as e:
            flash(f'Error: {e}')
            mysql.connection.rollback()
        finally:
            cur.close()

    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        EmployeeID = request.form['EmployeeID']

        if not EmployeeID:
            flash('Employee ID is required!')
            return redirect(url_for('delete'))

        cur = mysql.connection.cursor()
        try:
            cur.execute("DELETE FROM employee WHERE EmployeeID=%s", (EmployeeID,))
            mysql.connection.commit()
            flash('Record deleted successfully!')
        except Exception as e:
            flash(f'error: {e}')
            mysql.connection.rollback()
        
        finally:
            cur.close()

    return render_template('delete.html')

@app.route('/display')
def display():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    data = cur.fetchall()
    cur.close()
    return render_template('display.html', employees=data)



if __name__ == '__main__':
    app.run(debug=True)
