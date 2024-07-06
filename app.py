from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import string
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

DATABASE = 'personnel_management.db'

def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

#例如下方
random_num = generate_random_string()

# Generate random URLs once and store them in variables
add_user_url = f'/api/add_user/{random_num}'
edit_user_url_template = f'/api/edit_user/{random_num}/<int:user_id>'
delete_user_url_template = f'/api/delete_user/{random_num}/<int:user_id>'
get_users_url = f'/api/users/{random_num}'
get_user_url_template = f'/api/user/{random_num}/<int:user_id>'

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('setting.html', users=users, add_user_url=add_user_url, edit_user_url_template=edit_user_url_template, delete_user_url_template=delete_user_url_template, get_users_url=get_users_url, get_user_url_template=get_user_url_template)

@app.route(add_user_url, methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    name = data['name']
    role = data['role']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)', (username, password, name, role))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route(edit_user_url_template, methods=['POST'])
def edit_user(user_id):
    data = request.json
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    name = data['name']
    role = data['role']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET username = ?, password = ?, name = ?, role = ? WHERE id = ?', (username, password, name, role, user_id))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route(delete_user_url_template, methods=['POST'])
def delete_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route(get_users_url, methods=['GET'])
def get_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return jsonify([{'id': user[0], 'username': user[1], 'name': user[3], 'role': user[4]} for user in users])

@app.route(get_user_url_template, methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'id': user[0], 'username': user[1], 'name': user[3], 'role': user[4]})
    return jsonify({'status': 'not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
