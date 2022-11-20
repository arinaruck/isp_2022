import base64
import requests

# create a session
session = requests.session()

# perform a GET
session.get("http://127.0.0.1:5000/")

# perform a POST with a payload
session.post("http://127.0.0.1:5000/login",
             data={"username": "user", "password": "42"})

# inspect your cookies
print(session.cookies)

# modify your cookies
session.cookies.update({"LoginCookie": "admin"})
#session.cookies.update({"LoginCookie": base64.b64encode(b"admin").decode()})
r = session.get("http://127.0.0.1:5000/auth")
print(r.text)