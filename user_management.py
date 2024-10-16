import sqlite3
import hashlib
from flask import Flask, request

app = Flask(__name__)

# Función para generar el hash de la contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Función para almacenar un nuevo usuario
def store_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT)''')
    conn.commit()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Usuario ya registrado."
    finally:
        conn.close()
    return "Usuario registrado exitosamente"

# Función para validar un usuario
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    record = c.fetchone()
    conn.close()
    if record and record[0] == hash_password(password):
        return "Inicio de sesión exitoso"
    else:
        return "Usuario o contraseña incorrectos"

@app.route('/')
def index():
    return 'Bienvenido al sistema de gestión de usuarios'

# Ruta para registrar un nuevo usuario
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    return store_user(username, password)

# Ruta para validar usuario
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return validate_user(username, password)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7890)
