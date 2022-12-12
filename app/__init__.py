"""
Cold Embers: Sadi Nirloy, Emily Ortiz, Gabriel Thompson, Thomas Zhang
Software Development
p1: API Project ft. Database
2022-12-11
Time Spent: 
"""

from flask import Flask, session, render_template, request
import utl.table_handler as table_handler

app = Flask(__name__)
app.secret_key = os.urandom(32)

table_handler.setup() # setup tables

@app.route("/", methods = ["POST", "GET"])
def landing():
    if not 'username' in session:
        #if ()
    else:
        return render_template('landing.html')

@app.route("/registrate")
def registration()
    return render_template(landing.html)


if __name__ == "__main__":
    app.debug = True
    app.run()
