# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from connect import create_connection, close_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if authenticate_user(email, password):
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            return 'Login failed'
    return redirect(url_for('login_page'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        role = request.form['role']
        branch = request.form['branch']
        register_user(name, email, password, contact, role, branch)
        session['email'] = email
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' in session:
        email = session['email']
        user_data = fetch_user_data(email)
        if user_data:
            return render_template('profile.html', user_data=user_data)
    return 'You are not logged in'

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login_page'))

def authenticate_user(email, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT email, password FROM users WHERE email = %s"
    print("SQL Query:", query)
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    print("Values passed to SQL Query:", (email,))
    close_connection(connection)
    if user_data and user_data[1] == password:
        return True
    return False

def register_user(name, email, password, contact, role, branch):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, email, password, contact, role, branch) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (name, email, password, contact, role, branch))
    connection.commit()
    close_connection(connection)

def fetch_user_data(email):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT name, email, contact, role, branch FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    close_connection(connection)
    if user_data:
        return user_data
    return None

if __name__ == '__main__':
    app.run(debug=True)
