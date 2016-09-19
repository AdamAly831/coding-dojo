# ================================
# half of the time, when it says template not found check the spelling, and make sure the folder
# is TEMPLATES(lower), and not template

# ================================


from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
app.secret_key = 'ThisIsSecret'
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


# ================================

# Displays friends list 

# ================================
@app.route('/')
def index():
	friends = mysql.query_db("SELECT * FROM friends") #get the list of friends 
	return render_template('index.html', list=friends)

# ================================

# ADD FRIENDS

#Handle the add friend form submit and create the friend in the DB
# ================================

@app.route('/friends', methods=['POST'])
def create():
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(request.form['first_name'],request.form['last_name'],request.form['occupation'])
	data = {
           'first_name': request.form['first_name'], 
           'last_name': request.form['first_name'], 
           'occupation': request.form['first_name'], 

           }
	mysql.query_db(query, data)
	print query
	return redirect('/')
 
# ================================
# DISPLAYS FRIENDS LIST 

# Displays friends list for the particaluar friend 
# Handle the edit friend form submit and update the friend in the DB

# ================================
@app.route('/friends/<id>/edit', methods=['GET'])
def viewEdit(id):
    query = "SELECT * FROM friends WHERE id  = '{}'".format(id)
    friend = mysql.query_db(query)
    print friend
    return render_template('edit.html', friend=friend[0])# use this to populate the input

# ================================

#Handle the edit friend form submit and update the friend in the DB
#print the ID, update the query, with first, last occupation,  createed/updated at
	#update the query
# ================================

@app.route('/friends/<id>', methods=['POST'])
def  updateInfoInFriendsList(id):
	print id
	query = "UPDATE friends SET first_name = '{}', last_name = '{}', occupation = '{}',  created_at = NOW(), updated_at = NOW() WHERE id = {}".format(request.form['first_name'], request.form['last_name'], request.form['occupation'], int(id))
	mysql.query_db(query)
	return redirect('/')

# ================================

#Delete the friend from the DB

# ================================

@app.route('/friends/<id>/delete', methods=['POST'])
def delete(id):
	query = "DELETE FROM friends WHERE id = :id"
	data = {'id': id}
	mysql.query_db(query, data)
	return redirect('/')


app.run(debug=True)