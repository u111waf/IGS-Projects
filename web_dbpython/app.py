from flask import Flask, render_template, request
from flask_mysqldb import MySQL
#from config import Config
import os

app = Flask(__name__)
#app.config.from_object(Config)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_password'] = ''
app.config['MYSQL_DB'] = 'employeedb'

mysql = MySQL(app)

        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        EmployeeID =request.form['EmployeeID']
        Firstname = request.form['Firstname']
        Lastname= request.form['Lastname']
        Department= request.form['Department']
        Gender=request.form['Gender']
        Date = request.form['Date']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE employee SET Firstname=%s, Lastname=%s, Department=%s, Gender=%s, Date=%s WHERE EmployeeID=%s", (
                        Firstname,
                        Lastname,
                        Department,
                        Gender,
                        Date,
                        EmployeeID
                    ))
        mysql.connection.commit()

        cur.close()

        return 'success'



    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)
