from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_password'] = ''
app.config['MYSQL_DB'] = 'employeedb'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO users_table (Name, Email) VALUES (%s, %s)', (username, email))

        mysql.connection.commit()

        cur.close()

        return 'success'

    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()

    users = cur.execute('SELECT * FROM users_table')

    if users > 0:
        userDetails = cur.fetchall()

        return render_template('users.html', userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)