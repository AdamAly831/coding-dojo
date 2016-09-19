from flask import Flask, request, redirect, render_template, session, flash, escape
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = 'DojoNinjaSoSkeaky'
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app,'theWall')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# ==============================================================
#                           RENDER
# ==============================================================
@app.route('/')
def index():
    if 'user_id' in session and 'name' in session:
        return redirect('/wall')

    return render_template('index.html')

@app.route('/wall')
def wall():
    # validate session
    if 'user_id' in session and 'name' in session:

        # get messages
        queryStr = 'SELECT messages.id, text, messages.created_at, users.id as author_id, users.name as author FROM messages JOIN users ON messages.user_id = users.id ORDER BY created_at DESC';
        messages = mysql.query_db(queryStr)

        # get comments
        queryStr = 'SELECT comments.id, message_id, text, comments.created_at, users.id as author_id, users.name as author FROM comments JOIN users ON comments.user_id = users.id';
        comments = mysql.query_db(queryStr)

        # render the wall
        return render_template('wall.html', messages=messages, comments=comments)

    return redirect ('/')


app.run(debug=True)
