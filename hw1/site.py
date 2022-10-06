#!/usr/bin/env python3
import populate
from flask import Flask
from flask import request, jsonify
import pymysql
import math


app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"

# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.


@app.route("/messages", methods=["GET", "POST"])
def messages():
    name = request.form.get('name', None)
    print(f'name: {name}')
    with db.cursor() as cursor:
        if request.method == 'POST':
            if name:
                try:
                    query = "SELECT name, message FROM messages WHERE name=%s"
                    cursor.execute(query, (name,))
                except pymysql.err.ProgrammingError:
                    return {"Don't hack me, please!"}, 500
            else:
                return {'name argument must be passed for POST'}, 500
        else:
            query = "SELECT name, message FROM messages"
            cursor.execute(query)
        db.commit()
        res = cursor.fetchall()
        json = [{"name": n, "message": m} for n, m in res]
        return jsonify(json), 200


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.
@app.route("/users", methods=["GET"])
def contact():
    limit = request.args.get('limit', None)
    with db.cursor() as cursor:
        if limit:
            query = "SELECT name FROM users LIMIT %s"
            try:
                limit_n = int(limit)
                cursor.execute(query, (limit_n,))
            except (ValueError, pymysql.err.ProgrammingError):
                return {"Don't hack me, please!"}, 500
        else:
            query = "SELECT name FROM users"
            cursor.execute(query)
        db.commit()
        json = {"users": [row[0] for row in cursor.fetchall()]}
        return jsonify(json), 200


if __name__ == "__main__":
    db = pymysql.connect(host="localhost",
                         user=username,
                         password=password,
                         database=database,
                         charset="utf8mb4")
    with db.cursor() as cursor:
        populate.populate_db(cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)