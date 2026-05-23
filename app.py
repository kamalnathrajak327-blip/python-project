from flask import Flask, render_template, request,redirect,url_for,flash
#import pyodbc
import sqlite3
app=Flask(__name__)
app.secret_key = "secret123"

#database connection
#conn=pyodbc.connect('Driver={SQL Server};'
                   # 'Server=DESKTOP-1UMSK0Q\\KAMAL_LOCAL;'
                    #'Database=kamal;'
                    #'Trusted_Connection=yes;')
#cursor=conn.cursor()


conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    gmail TEXT,
    password TEXT,
    gender TEXT
)
''')
conn.commit()


print("connection successful")
#home page
@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        gmail = request.form['gmail']
        password = request.form['password']
        #password validation
        if len(password) < 8:
                flash("Password must be at least 8 characters ❌")
                return redirect(url_for('home'))
        else:
            cursor.execute("SELECT * FROM users WHERE gmail=? AND password=?", (gmail, password))
            user = cursor.fetchone()
            #check if user exists
            if user:
                return render_template('wellcome.html', valid=" Login successful ✅")
            else:
                flash("Invalid email or password ❌")
                return redirect(url_for('home'))

    return render_template('index.html')

#registration page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['gmail']
        password = request.form['password']
        confirm_password = request.form['confim_password']
        gender = request.form['gender']
 
        #password validation
        if len(password) < 8:
                flash("Password must be at least 8 characters ❌")
                return redirect(url_for('signup'))
        else:
            #check password and confirm password match
            if password != confirm_password:
                flash("Passwords do not match ❌")
                return redirect(url_for('signup'))
           
            else:
                cursor.execute("INSERT INTO users (first_name, last_name, gmail, password, gender) values (?, ?, ?, ?, ?)", (first_name, last_name, email, password, gender))
                conn.commit()
                flash("Data Saved Successfully ✅")
                return redirect(url_for('home'))     
        
    return render_template('signup.html')

#password update page
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['gmail']
        new_password = request.form['password']
        #password validation
        if len(new_password) < 8:
                flash("Password must be at least 8 characters ❌")
                return redirect(url_for('forgot'))
        else:
                #password update query
                cursor.execute("UPDATE users SET password=? WHERE gmail=?", (new_password, email))
                conn.commit()
                flash("Password updated successful ✅ Please login")
                return redirect(url_for('home'))   

    return render_template('forgot.html')


#app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
