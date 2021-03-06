# https://pythonhosted.org/Flask-JWT/

import hashlib

from flask import Flask, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

# Get the app and mysql info
from app import app
from app.db import mysql

# From flask-JWT website example
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

# Route is /auth
def authenticate(username, password):
    # Use conn and cursor outside of try block
    conn = mysql.connect()
    cursor = mysql.get_db().cursor()
    try:
        cursor.execute("SELECT salt from user_info where email = %s", (username))
        rows = cursor.fetchone()
        p = str(password) + str(rows[0])
        hash = hashlib.sha256()
        hash.update(p.encode('utf-8').decode('latin1').encode())
        p = hash.hexdigest()
        cursor.execute("SELECT id, email, password FROM user_info where email = %s", (username))
        rows = cursor.fetchall()
        if rows:
            user = User(rows[0][0], rows[0][1], rows[0][2])
            if user and safe_str_cmp(user.password, p):
                return user
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

def identity(payload):
    user_id = payload['identity']
    conn = mysql.connect()
    cursor = mysql.get_db().cursor()
    try:
        cursor.execute("SELECT id, email, password FROM user_info where id = %s", (user_id))
        rows = cursor.fetchall()
        if rows:
            user = User(rows[0][0], rows[0][1], rows[0][2])
            return user
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)

# Define route to get userid
@app.route('/userid')
@jwt_required()
def userid():
    return '%s' % current_identity
