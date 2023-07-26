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
  "measurementId": "G-NLCR9J0H4T",
  "databaseURL": "https://individual-project-y2-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user= {"username": username}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('index'))
        except:
            return redirect(url_for('signin'))
   return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       # username = request.form['username']
       email = request.form['email']
       password = request.form['password']
       try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('todos'))
       except:
        error = "failed?????"
   return render_template("signin.html")
@app.route('/todos', methods=['GET', 'POST'])
def todos():
    UID = login_session['user']['localId']
    if request.method=="POST":
        task = request.form['task']
        Tasks= {"task": task}
        db.child("Users").child(UID).child("Tasks").push(Tasks)
    taskdesplay= db.child("Users").child(UID).child("Tasks").get().val()
    if taskdesplay!=None:
        return render_template("todos.html", tasks=taskdesplay)
    else: 
        return render_template("todos.html")

@app.route('/delete/<string:i>')
def funct(i):
    UID = login_session['user']['localId']
    db.child("Users").child(UID).child("Tasks").child(i).remove()
    return redirect(url_for("todos"))



# @app.route('/signout')
# def signout():
#     login_session['user'] = None
# auth.current_user = None
# return redirect(url_for('signin'))






#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)