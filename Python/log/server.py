from flask import Flask, request, redirect, render_template, session, flash, escape
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = 'Dojothing'
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app,'theWall')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# ==============================================================
#                           RENDER
# ==============================================================

@app.route('/')
def index():
    # if the user has loged in redirect them to the wall if not they will stay at the log in 
    if 'user_id' in session and 'name' in session:
        return redirect('/wall')

    return render_template('index.html')

@app.route('/wall')
def wall():
    # validate session
    if 'user_id' in session and 'name' in session:

        # get messages
        query = 'SELECT messages.id, text, messages.created_at, users.id as author_id, users.name as author FROM messages JOIN users ON messages.user_id = users.id ORDER BY created_at DESC';
        messages = mysql.query_db(query)

        # get comments
        query = 'SELECT comments.id, message_id, text, comments.created_at, users.id as author_id, users.name as author FROM comments JOIN users ON comments.user_id = users.id';
        comments = mysql.query_db(query)

        # render the wall
        return render_template('wall.html', messages=messages, comments=comments)

    return redirect ('/')
# ==============================================================
#                       LOGIN & REGISTRATION
# ==============================================================
@app.route('/users/login', methods = ['POST'])
def login():
    # because it's shorter
    post = request.form
    print post

    # test for post data
    if 'email' in post and 'password' in post:

        # escape inputs
        email = escape(post['email']).lower()#changes the email to lower case 
        password = escape(post['password'])

        # test for valid inputs
        if email and password:

            # see if a user with 'email' exists
            query = 'SELECT * FROM users WHERE email = :email'
            data = {'email': email}
            user = mysql.query_db(query, data)

            # if there is a user with 'email'
            if user:

                # test password
                if bcrypt.check_password_hash(user[0]['password'], password):

                    # set session and go to the wall
                    session['user_id'] = int(user[0]['id'])
                    session['name'] = user[0]['name']

                    return redirect('/wall')


            flash("email and password dosn't match", 'lg_email')

        # set errors for empty inputs
        else:
            if not post['email']: flash("Email cannot be blank", 'lg_email')
            if not post['password']: flash("Password cannot be blank", 'lg_password')

    # if it failed reload the login page
    return redirect('/')


@app.route('/users', methods = ['post'])
def create ():
    post = request.form
    # test for post data
    if 'name' in post and 'email' in post and 'password' in post and 'passwordConfirm' in post:

        # escape inputs
        name = escape(post['name'])
        email = escape(post['email'])
        password = escape(post['password'])
        passwordConfirm = escape(post['passwordConfirm'])

        #setting err= to false beucase i can 
        err = False

        # validate inputs
        if not name:
            err = True #false = true 
            flash("Name can't  be blank", "name")
        if not email:
            err = True #false = true 
            flash("Email can't be blank", "email")
        elif not EMAIL_REGEX.match(email):
            err = True #false = true 
            flash("Invalid email address", "email")
        if not password:
            err = True #false = true 
            flash("Password can't be blank", "password")
        if not passwordConfirm:
            err = True #false = true 
            flash("Password Confirmation can't be blank", "passwordConfirm")
        if password and passwordConfirm and password != passwordConfirm: # if the combinatoin of passwords do not match 
            err = True #false = true 
            flash("Passwords do not match", "password")


        # if there were no errors
        if not err: # if there is no flase 

            # encrypt password
            encrypted_password = bcrypt.generate_password_hash(password)

            # insert user
            query = "INSERT INTO Users (name, email, password, created_at, updated_at) VALUES (:name, :email, :password, NOW(), NOW())"
            data = {'name': name.lower(),'email': email, 'password': encrypted_password}
            user_id = mysql.query_db(query, data)

            # set session
            session['user_id'] = int(user_id)
            session['name'] = name
            return redirect('/wall')

    # if it failed reload the login page
    return redirect('/')

@app.route('/logout')
def logout():
    # clear our session variables
    session.pop('user_id', None)
    session.pop('name', None)

    # redirect to login
    return redirect('/')


app.run(debug=True)
