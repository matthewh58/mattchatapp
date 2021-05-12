import sqlite3
import time
import smtplib
from flask import *
from groups import *
from user import *
from message import *

app = Flask(__name__)

@app.route("/")
def test():
    return "test"

@app.route("/users")
def getUsers():
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select rowid, username, password, image, created_time from user")
    results = c.fetchall()
    users = []
    for r in results:
        users.append(User(r[0], r[1], r[2], r[3], r[4]))
    return json.dumps([ob.__dict__ for ob in users])


@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select rowid, username, password from user where username = ? and password = ? ", (username, password))
    results = c.fetchall()
    if len(results) > 0:
        return {"result": results[0][0]}
    else:
        return {"result": -1}


@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("insert into user(username, password, created_time) values(?,?,?)", (username, password, int(time.time())))
    con.commit()
    return {"result": c.lastrowid}

@app.route("/messages", methods=["POST"])
def messages():
    user1 = request.json["user1"]
    user2 = request.json["user2"]
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select u1.rowid, u1.username, u1.image, message, time from message, user u1 where u1.rowid = user1 and ((user1 = ? and user2 = ?) or (user1 = ? and user2 = ?))", (user1, user2, user2, user1))
    messages = []
    results = c.fetchall()
    for r in results:
        messages.append(Message(r[0], r[1], r[2], r[3], r[4]))
    return json.dumps([ob.__dict__ for ob in messages])


@app.route("/send", methods=["POST"])
def send():
    user1 = request.json["user1"]
    user2 = request.json["user2"]
    message = request.json["message"]
    t = int(time.time())
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("insert into message(user1, user2, message, time) values(?,?,?,?)", (user1, user2, message, t))
    con.commit()
    return ""

@app.route("/user/<id>")
def getUser(id):
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select username, password, image, created_time from user where rowid = ?", (id))
    result = c.fetchall()[0]
    u = User(0, result[0], result[1], result[2], result[3])
    return json.dumps(u.__dict__)

@app.route("/updateuser", methods=["POST"])
def updateUser():
    image = request.json["image"]
    userId = request.json["userId"]
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("update user set image = ? where rowid = ?", (image, userId))
    con.commit()
    return ""


@app.route("/updateuserdata", methods=["POST"])
def updateUserData():
    image = request.json["image"]
    username = request.json["username"]
    newPassword = request.json["newPassword"]
    userId = request.json["userId"]
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("update user set image = ?, password = ?, username = ? where rowid = ?", (image, newPassword, username, userId))
    con.commit()
    return ""

@app.route("/verify", methods=["POST"])
def verify():
    email = request.json["email"]
    passcode = request.json["passcode"]
    username = request.json["username"]
    password = request.json["password"]
    confirmPassword = request.json["confirmPassword"]
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select username from user where username = '" + username + "'")
    results = c.fetchall()
    if len(results) > 0:
        return {"result": -1}
    if confirmPassword != password:
        return {"result": -2}

    msg = """\
    Subject: Verify Email


    Your verification code for matthew's chat app is: 
    """ + passcode

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('matthewsspamacc@gmail.com', 'jimbob2022')
    server.sendmail('matthewsspamacc@gmail.com', email, msg)
    server.close()

    return {"result": 1}


@app.route("/groups")
def groups():
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select rowid, name, description, image, created_time from groups")
    results = c.fetchall()
    groups = []
    for r in results:
        groups.append(Groups(r[0], r[1], r[2], r[3], r[4]))
    return json.dumps([ob.__dict__ for ob in groups])


@app.route("/group/<id>")
def group(id):
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select rowid, name, description, image, created_time from groups where rowid = " + str(id))
    r = c.fetchall()[0]
    group = Groups(r[0], r[1], r[2], r[3], r[4])
    return json.dumps(group.__dict__)


@app.route("/groupmessage", methods=["POST"])
def groupMessage():
    group_id = request.json["groupId"]
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("select u.rowid, u.username, u.image, message, time from group_message gm, user u where u.rowid = gm.user_id and gm.group_id = " + str(group_id))
    messages = []
    results = c.fetchall()
    for r in results:
        messages.append(Message(r[0], r[1], r[2], r[3], r[4]))
    return json.dumps([ob.__dict__ for ob in messages])

@app.route("/sendgroupmessage", methods=["POST"])
def sendGroupMessage():
    user_id = request.json["userId"]
    group_id = request.json["groupId"]
    message = request.json["message"]
    t = int(time.time())
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("insert into group_message(user_id, group_id, message, time) values(?,?,?,?)", (user_id, group_id, message, t))
    con.commit()
    return ""

@app.route("/creategroup", methods=["POST"])
def createGroup():
    group_name = request.json["groupName"]
    group_description = request.json["groupDescription"]
    group_image = request.json["groupImage"]
    t = int(time.time())
    con = sqlite3.connect("messenger.db")
    c = con.cursor()
    c.execute("insert into groups(name, description, image, created_time) values (?,?,?,?)", (group_name, group_description, group_image, t))
    con.commit()
    return ""


if __name__ == '__main__':

    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)