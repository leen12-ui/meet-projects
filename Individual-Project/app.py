from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyDYaEd6GchS0theUwbl5r2n5-o_CDmbLKQ",
  "authDomain": "individual-project-y2.firebaseapp.com",
  "projectId": "individual-project-y2",
  "storageBucket": "individual-project-y2.appspot.com",
  "messagingSenderId": "33729504278",
  "appId": "1:33729504278:web:d34c4874500e26a7954137",
  "measurementId": "G-NLCR9J0H4T"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
       username = request.form['username']
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = 
auth.create_user_with_email_and_password(username,email, password)
           return redirect(url_for('index'))
       except:
   return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = 
auth.sign_in_with_email_and_password(email, password)
           return redirect(url_for('home'))
       except:
           error = "Authentication failed"
   return render_template("signin.html")
# @app.route('/signout')
# def signout():
#     login_session['user'] = None
# auth.current_user = None
# return redirect(url_for('signin'))






#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)