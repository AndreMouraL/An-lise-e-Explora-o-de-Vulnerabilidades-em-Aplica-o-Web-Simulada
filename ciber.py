pip install flask

/flask-vuln-app
├── app.py
├── templates/
│   ├── index.html
│   └── login.html
└── static/
    └── style.css
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave para manter a sessão

# Conexão com o banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('vulnerable.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de login com vulnerabilidade de SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerabilidade de SQL Injection
        conn = get_db_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        
        if user:
            session['user'] = username
            return redirect(url_for('welcome'))
        else:
            return "Invalid credentials!"
    
    return render_template('login.html')

# Página de boas-vindas
@app.route('/welcome')
def welcome():
    if 'user' in session:
        return f'Welcome {session["user"]}!'
    return redirect(url_for('login'))

# Criar banco de dados e adicionar um usuário (não seguro)
@app.route('/create_db')
def create_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.execute('INSERT INTO users (username, password) VALUES ("admin", "password123")')
    conn.commit()
    conn.close()
    return "Database created and user added."

if __name__ == '__main__':
    app.run(debug=True)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vulnerable Web App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Welcome to the Vulnerable Web Application</h1>
    <a href="{{ url_for('login') }}">Login</a>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Login</h1>
    <form method="POST">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        
        <button type="submit">Login</button>
    </form>
</body>
</html>
body {
    font-family: Arial, sans-serif;
    padding: 20px;
    background-color: #f4f4f4;
}

h1 {
    color: #333;
}

a {
    color: #0066cc;
    text-decoration: none;
}

form {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 300px;
    margin: 0 auto;
}

label {
    font-weight: bold;
}

button {
    background-color: #28a745;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

# Execute isso para criar o banco de dados e adicionar um usuário "admin"
import sqlite3

conn = sqlite3.connect('vulnerable.db')
conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
conn.execute('INSERT INTO users (username, password) VALUES ("admin", "password123")')
conn.commit()
conn.close()

python app.py
