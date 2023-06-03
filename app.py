from flask import Flask, render_template, request, redirect, session, make_response
import os
import random
import string

app = Flask(__name__)
users_folder = 'users_data'

# Specify the paths to the SSL certificate and private key files
ssl_cert_path ='/root/messageBoard/certificate.crt'
ssl_key_path ='/root/messageBoard/private.key'

if not os.path.exists(users_folder):
    os.makedirs(users_folder)

# Generate or load the secret key
secret_key_file = 'secret_key.txt'

if not os.path.exists(secret_key_file):
    secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    with open(secret_key_file, 'w') as file:
        file.write(secret_key)
else:
    with open(secret_key_file, 'r') as file:
        secret_key = file.read()

app.secret_key = secret_key


@app.route('/')
def index():
    if 'username' in session:
        return redirect('/message_board')
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_user_registered(username):
            save_user_data(username, password)
            session['username'] = username  # Update session with new user
            return redirect('/message_board')
        else:
            return render_template('register.html', error='Username already exists.')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if is_valid_credentials(username, password):
            session['username'] = username
            return redirect('/message_board')
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')


@app.route('/message_board', methods=['GET', 'POST'])
def message_board():
    if 'username' in session:
        username = session['username']
        password_file = get_password_file(username)
        messages_file = get_messages_file(username)

        if request.method == 'POST':
            message = request.form['message']
            with open(messages_file, 'a') as file:
                file.write(message + '\n')

        messages = get_user_messages(username)
        return render_template('message_board.html', username=username, messages=messages)

    return redirect('/login')


@app.route('/clear', methods=['POST'])
def clear():
    if 'username' in session:
        username = session['username']
        messages_file = get_messages_file(username)
        with open(messages_file, 'w') as file:
            file.truncate()
        return redirect('/message_board')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect('/login'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


def is_user_registered(username):
    password_file = get_password_file(username)
    return os.path.exists(password_file)


def save_user_data(username, password):
    password_file = get_password_file(username)
    with open(password_file, 'w') as file:
        file.write(password)


def is_valid_credentials(username, password):
    password_file = get_password_file(username)
    if os.path.exists(password_file):
        with open(password_file, 'r') as file:
            stored_password = file.read().strip()
        return password == stored_password
    return False


def get_password_file(username):
    return os.path.join(users_folder, f'{username}_password.txt')


def get_messages_file(username):
    return os.path.join(users_folder, f'{username}_messages.txt')


def get_user_messages(username):
    messages_file = get_messages_file(username)
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as file:
            messages = file.read().strip().split('\n')
        return messages
    return []


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=80)
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context=(ssl_cert_path, ssl_key_path))

