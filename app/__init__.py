from flask import Flask, session, render_template, request
import sqlite3
import utl.table_handler as table_handler
import utl.api_handler as api_handler

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('landing.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
