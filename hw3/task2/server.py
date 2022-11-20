from flask import Flask, request, make_response
import base64
import hashlib
import hmac
import random
import binascii

app = Flask(__name__)

cookie_name = "LoginCookie"
API_SECRET = b'892374928347928347283473'
N_DIGITS = 10


def generate_session_id():
    lower = 10**(N_DIGITS-1)
    upper = 10**N_DIGITS - 1
    session_id_num = random.randint(lower, upper)
    return str(session_id_num)

def is_admin(username, password):
    return (username == "admin") and (password == "42")

def get_hmac(username, session_id, user_type):
    message = str.encode(' '.join([username, session_id, user_type]))
    signature = hmac.new(
        API_SECRET,
        msg=message,
        digestmod=hashlib.sha256
    ).hexdigest().upper()
    return signature

@app.route("/login",methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']
    user_type = 'admin' if is_admin(username, password) else 'user'
    response = make_response()
    session_id = generate_session_id()
    HMAC = get_hmac(username, session_id, user_type)
    cookie = str.encode(f'{username},{session_id},com402,hw3,ex2,{user_type},{HMAC}')
    response.set_cookie(cookie_name, base64.b64encode(cookie).decode('utf-8'))
    return response 

@app.route("/auth",methods=['GET'])
def auth():
    cookie_enc = request.cookies.get(cookie_name)
    try:
        cookie = base64.b64decode(cookie_enc).decode()
        username, session_id, _, _, _, user_type, hmac = cookie.split(',')
    except (ValueError, binascii.Error):
        return {}, 403
    if get_hmac(username, session_id, user_type) != hmac:
        return {}, 403
    if user_type == 'admin':
        return {}, 200
    if user_type == 'user':
        return {}, 201 

if __name__ == '__main__':
    app.run()