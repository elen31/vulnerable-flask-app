from flask import Flask, request, render_template_string, redirect, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <h2>Welcome!</h2>
        <ul>
            <li><a href="/login">Login</a></li>
            <li><a href="/xss">XSS Test</a></li>
            <li><a href="/upload">File Upload</a></li>
            <li><a href="/idor?id=1">IDOR Example</a></li>
            <li><a href="/profile">User Profile (Broken Auth)</a></li>
        </ul>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = '''
    <form method="POST">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <input type="submit">
    </form>
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = conn.execute(query).fetchone()
        conn.close()
        if result:
            return f"<h3>Welcome, {username}! <a href='/profile'>Go to Profile</a></h3>"
        else:
            return render_template_string(form + "<p>Invalid credentials</p>")
    return render_template_string(form)

@app.route('/xss', methods=['GET', 'POST'])
def xss():
    form = '''
    <form method="POST">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <input type="submit">
    </form>
    '''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        return f"<h3>Hello {username}</h3><p>Your password is {password}</p>{form}"
    return form

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit">
    </form>
    '''
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename  # Insecure: no sanitization
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return f"File uploaded: <a href='/uploads/{filename}'>{filename}</a>"
    return form

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/idor')
def idor():
    user_id = request.args.get('id', '1')
    conn = sqlite3.connect('users.db')
    result = conn.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()
    conn.close()
    return f"<h3>User Info: {result}</h3>"

@app.route('/profile')
def profile():
    return '''
        <h3>User Profile (Broken Auth)</h3>
        <p>Welcome, admin!</p>
        <p>Email: admin@example.com</p>
        <p>Phone: 123-456-7890</p>
        <p><i>(No session check, this is broken!)</i></p>
    '''

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = '''
    <h3>Change Admin Password</h3>
    <form method="POST">
        New Password: <input name="new_password"><br>
        <input type="submit" value="Change">
    </form>
    '''
    if request.method == 'POST':
        new_password = request.form['new_password']
        conn = sqlite3.connect('users.db')
        conn.execute("UPDATE users SET password=? WHERE username='admin'", (new_password,))
        conn.commit()
        conn.close()
        return f"<p>Password changed to: <b>{new_password}</b></p>{form}"
    return form

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
