from flask import Flask, render_template  # Import Flask to allow us to create our app, and import
                                          # render_template to allow us to render index.html.
app = Flask(__name__)                     # Global variable __name__ tells Flask whether or not we
                                          # are running the file directly or importing it as a module.
@app.route('/')                           # The "@" symbol designates a "decorator" which attaches the
def index():
	return render_template('index.html')

@app.route('/ninjas')
def ninjas():
	return render_template('ninjas.html')

@app.route('/dojos')
def dojos():
	return render_template('dojos.html')

app.run(debug=True)                        
