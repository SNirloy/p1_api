"""
Cold Embers: Sadi Nirloy, Emily Ortiz, Gabriel Thompson, Thomas Zhang
Software Development
p1: API Project ft. Database
2022-12-11
Time Spent: 
"""

from flask import Flask, session, render_template, request, redirect, flash
import os
import utl.table_handler as table_handler
import utl.api_handler as api_handler

app = Flask(__name__)
app.secret_key = os.urandom(32)

table_handler.setup() # setup tables

@app.route("/", methods = ["POST", "GET"])
def landing():
    logged_in = ('username' in session)
    username = ''

    if 'username' in session:
        username = session['username']

    return render_template('landing.html', logged_in=('username' in session), username=username)

@app.route("/register", methods = ['GET', 'POST'])
def register_page():
    return render_template('register.html')

@app.route("/registrate", methods = ['GET', 'POST'])
def registration():
    if (table_handler.registrate(request.form["createusername"], request.form["createpassword"]) == False):
        flash("That username is already taken", "danger")
        return render_template('register.html')
    else:
        return render_template('login.html', message = "Account created!")

@app.route("/login", methods = ['GET', 'POST'])
def loginpage():
    return render_template('login.html')

@app.route("/verify", methods = ['GET', 'POST'])
def login():
    if (table_handler.user_check(request.form["username"]) == True):
        if (table_handler.password_check(request.form["username"], request.form["password"]) == True):
            session['username'] = request.form['username']
            return redirect('/')
        else:
            return render_template('login.html' , message = "Invalid username/password")
    else: 
        return render_template('login.html', message = "invalid username/password")

@app.route("/view_places")
def view_places():
    airport_name = request.args['airport']
    airport_code = airport_name[-4:-1]
    print('Airport: ' + airport_code)
    coords = api_handler.airport_api(airport_code) 
    print('='*50 + " AIRPORT " + "="*50)
    print(coords)


    yelp_results = api_handler.yelp_api(coords)
    print('='*50 + " YELP " + "="*50)
    print(yelp_results)

    return render_template('view_places.html', yelp_results=yelp_results)

@app.route("/airport")
def airport():
    c = api_handler.airport_api(request.form["airport_code"])
    return render_template('view_places.html', airport_coordinate = c)

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()
