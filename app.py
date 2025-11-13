from flask import Flask, render_template, request, redirect, url_for, session
from Database import get_connection
import os

app = Flask(__name__)
app.secret_key = 'secretnilord'


@app.route('/')
def main():
    return render_template('Main.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/home')
def home():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password."
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return "Username or email already exists!"

        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """, (username, email, password))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT username, email, contact FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT",5000)))


