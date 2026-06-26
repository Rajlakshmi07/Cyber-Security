from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key"

bcrypt = Bcrypt(app) 

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db() 

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        username=request.form["username"]

        password=request.form["password"]

        hashed=bcrypt.generate_password_hash(password).decode("utf-8")

        conn=sqlite3.connect("users.db")
        cur=conn.cursor()

        try:
            cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,hashed))
            conn.commit()
            conn.close()

            return redirect("/login")

        except:
            conn.close()
            return "Username already exists."

    return render_template_string("""

    <h2>Register</h2>

    <form method="POST">

    Username:<br>
    <input name="username"><br><br>

    Password:<br>
    <input type="password" name="password"><br><br>

    <button>Register</button>

    </form>

    <a href="/login">Login</a>

    """)

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]

        password=request.form["password"]

        conn=sqlite3.connect("users.db")
        cur=conn.cursor()

        cur.execute("SELECT password FROM users WHERE username=?",(username,))
        user=cur.fetchone()

        conn.close()

        if user and bcrypt.check_password_hash(user[0],password):

            session["user"]=username

            return redirect("/dashboard")

        else:
            return "Invalid Username or Password"

    return render_template_string("""

    <h2>Login</h2>

    <form method="POST">

    Username<br>
    <input name="username"><br><br>

    Password<br>
    <input type="password" name="password"><br><br>

    <button>Login</button>

    </form>

    <a href="/register">Register</a>

    """)

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template_string("""

    <h2>Welcome {{name}}</h2>

    <a href="/logout">Logout</a>

    """,name=session["user"]) 

@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect("/login") 

if __name__=="__main__":
    app.run(debug=True)
