import mysql.connector as mariadb
from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secret'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

mydb = mariadb.connect(user='root', database='forum_db')
mycursor = mydb.cursor()


@app.route('/comments', methods=['DELETE'])
def delete_comment():
    print (request.get_json())
    cid = request.get_json()['comid']
    email = request.get_json()['useremail']
    mycursor.execute("SELECT * FROM Forum_users WHERE email = " + "'" + str(email) + "'" )
    rv = mycursor.fetchone()
    uid = rv[0]
    mycursor.execute("SELECT * FROM Comments WHERE comment_id = " + str(cid))
    rv2 = mycursor.fetchone()
    result = {'error': 'Error'}
    if rv2[1] == uid:
        sql = "DELETE FROM Comments WHERE comment_id = " + str(cid)
        mycursor.execute(sql)
        mydb.commit()
        result = {
            'comid': cid
        }
    else:
        result = {'error': 'Error'}
    
    return jsonify({'result': result})


@app.route('/comments', methods=['PUT'])
def create_comment():
    pid = request.get_json()['pid']
    info = request.get_json()['text']
    email = request.get_json()['usermail']
    mycursor.execute("SELECT * FROM Forum_users WHERE email = " + "'" + str(email) + "'" )
    rv = mycursor.fetchone()
    uid = rv[0]

    sql = "INSERT INTO Comments (user_id, p_id, " + " text " + ")  \
    VALUES (" + str(uid) + "," + str(pid) + "," + "'" + str(info) + "'" + ")"
    
    mycursor.execute(sql)
    mydb.commit()

    result = {
        'uid': uid,
        'pid': pid,
        'text': info
    }

    return jsonify({'result': result})

@app.route('/comments', methods=['POST'])
def get_comments():
    print ('- - - - - - - - - - - - - -- - - - -  --')
    print(request.get_json())
    pid = request.get_json()['pid']
    mycursor.execute("SELECT * FROM Comments WHERE p_id = " + str(pid))
    rv = mycursor.fetchall()
    print (rv)
    l = []
    for x in rv:
        l.append({'id': x[0],
            'cuser': x[1],
            'pid': x[2],
            'text': x[3]})

    for i in range(len(l)):
        user = l[i]['cuser']
        mycursor.execute("SELECT * FROM Forum_users WHERE id = " + str(user))
        rv = mycursor.fetchone()
        l[i]['cuser'] = rv[1]

    return jsonify({'result': l})


@app.route('/', methods=['DELETE'])
def delete_post():
    print (request.get_json())
    pid = request.get_json()['postid']
    email = request.get_json()['useremail']
    mycursor.execute("SELECT * FROM Forum_users WHERE email = " + "'" + str(email) + "'" )
    rv = mycursor.fetchone()
    uid = rv[0]
    mycursor.execute("SELECT * FROM Posts WHERE post_id = " + str(pid))
    rv2 = mycursor.fetchone()
    result = {'error': 'Error'}
    if rv2[1] == uid:
        sql = "DELETE FROM Posts WHERE post_id = " + str(pid)
        mycursor.execute(sql)
        mydb.commit()
        result = {
            'postid': pid
        }
    else:
        result = {'error': 'Error'}
    
    return jsonify({'result': result})


@app.route('/', methods=['PUT'])
def create_post():
    domid = request.get_json()['domainid']
    info = request.get_json()['postinfo']
    email = request.get_json()['useremail']
    mycursor.execute("SELECT * FROM Forum_users WHERE email = " + "'" + str(email) + "'" )
    rv = mycursor.fetchone()
    uid = rv[0]

    sql = "INSERT INTO Posts (puser, pdomain, content) \
    VALUES (" + str(uid) + "," + str(domid) + "," + "'" + str(info) + "'" + ")"
    
    mycursor.execute(sql)
    mydb.commit()

    result = {
        'puser': uid,
        'pdomain': domid,
        'content': info
    }

    return jsonify({'result': result})

@app.route('/posts', methods=['GET'])
def get_posts():
    mycursor.execute("SELECT * FROM Posts")
    rv = mycursor.fetchall()
    print (rv)
    l = []
    for x in rv:
        l.append({'id': x[0],
            'puser': x[1],
            'pdomain': x[2],
            'content': x[3]})

    for i in range(len(l)):
        user = l[i]['puser']
        mycursor.execute("SELECT * FROM Forum_users WHERE id = " + str(user))
        rv = mycursor.fetchone()
        l[i]['puser'] = rv[1]

        domain = l[i]['pdomain']
        mycursor.execute("SELECT * FROM Domains WHERE domain_id = " + str(domain))
        rv = mycursor.fetchone()
        l[i]['pdomain'] = rv[1]

    return jsonify({'result': l})


@app.route('/', methods=['GET'])
def get_domains():
    mycursor.execute("SELECT * FROM Domains")
    rv = mycursor.fetchall()
    print (rv)
    l = []
    for x in rv:
        l.append({'id': x[0],
            'name': x[1],
            'duser': x[2],
            'ddesc': x[3]})

    result = {'result': l}
    return jsonify({'result': l})


@app.route('/users/register', methods=['POST'])
def register():
    username = request.get_json()['username']
    email = request.get_json()['email']

    mycursor.execute("SELECT * FROM Forum_users where email = '" + str(email) + "'")
    rv = mycursor.fetchone()
    if rv != None:
        return None

    # password = bcrypt.generate_password_hash(
    #     request.get_json()['password']).decode('utf-8')
    password = request.get_json()['password']
    job = request.get_json()['job']
    
    sql = "INSERT INTO Forum_users (user_name, pass, email, rol_id, job) \
    	VALUES ('" + str(username) + "','" + str(password) + "','" + str(email) + "','" + '1' + "','" + '1' + "')"
    mycursor.execute(sql)
    mydb.commit()

    result = {
        'user_name': username,
        'pass': password,
        'email': email,
        'job': job
    }

    return jsonify({'result': result})


@app.route('/users/login', methods=['POST'])
def login():
    print ('ok')
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = None

    mycursor.execute("SELECT * FROM Forum_users where email = '" + str(email) + "'")
    rv = mycursor.fetchone()
    print ('* * * * * * * * * * * * * * *')
    print(rv)
    #print (password)
    #print (rv[2])
    print ('* * * * * * * * * * * * * * *')
    if rv == None:
        return result
    if rv[2] == password: #bcrypt.check_password_hash(rv[2], password):
        access_token = create_access_token(
            identity={
                'username': rv[1],
                'email': rv[3]
            })
        result = access_token
    else:
        result = None

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
