from flask import Flask, session, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('landing.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
