from flask import Flask, render_template, request, redirect, session  
import random
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'


@app.route('/')
def index():
  return render_template("index.html")

@app.route('/guess', methods=['POST'])
def guess():
	#setting randome number
	if 'rand' not in session:
		session['rand'] = random.randrange(1,101)
 	guess = int (request.form ['guess'])

	if guess < session ['rand']:
		session['guess'] = "too_low"
	elif guess>session ['rand']:
		session['guess'] = "too_high"
	else: 
		session['guess'] = "correct"
			 

	return redirect('/')

@app.route('/reset', methods= ["POST"])
def reset():
	session.clear()
	return redirect('/')

app.run(debug=True)


 