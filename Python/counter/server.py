from flask import Flask, render_template, request, redirect, session  
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'


# increment count by 1 FUNCATION
# get the @app.rout and (/) ((increment and use the post methode( mabey???))
# def  the index
# add session count +=1
# return render template + index and  count=session['count'] 

@app.route('/')
def index():
  if 'count' in session: 
    session['count'] +=1
  else:
    session['count'] = 1 # count is a key in the dictionary 
  return render_template('index.html', count=session['count'])
 
@app.route('/increment', methods=['POST'])
def increment_by_two():
    session['count'] += 1
    #We only increment by 1 since reloading the page also increments
    return redirect('/')
    
@app.route('/clear', methods=['POST'])
def clear():
    session['count'] = 0
    return redirect('/')
 

app.run(debug=True)