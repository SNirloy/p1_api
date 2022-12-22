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
        return render_template('login.html')

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
            flash("Invalid username/password", "danger")
            return render_template('login.html')
    else: 
        flash("Please enter your username/password", "danger")
        return render_template('login.html')

@app.route("/view_places")
def view_places():
    if not 'username' in session:
        flash("Please log in or register first", "danger")
        return redirect('/login')
    else: 
        airport_name = request.args['airport']
        airport_code = airport_name[-4:-1]
        print('Airport: ' + airport_code)
        coords = api_handler.airport_api(airport_code) 
        print('='*50 + " AIRPORT " + "="*50)
        print(coords)


        yelp_results = api_handler.yelp_api(coords)
        print('='*50 + " YELP " + "="*50)
        print(yelp_results)

        hotel_results = api_handler.booking_api(coords + [request.args['date1'], request.args['date2']])
        print('='*50 + " HOTEL " + "="*50)
        print(hotel_results)

        lat, lon = coords[0], coords[1]
        left = lon - 0.1
        right = lon + 0.1
        down = lat - 0.1
        up = lat + 0.1
        bbox = f"{left}%2C{down}%2C{right}%2C{up}"

        return render_template('view_places.html', yelp_results=yelp_results, hotel_results=hotel_results, bbox=bbox)

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()
