import sqlite3
import time
from flask import Flask, g, request, render_template, redirect

app = Flask(__name__)
DATABASE = 'cheeps.db'

#Get the database.
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Read the cheeps from the DB.
def db_read_cheeps():
	cur = get_db().cursor()
	cur.execute("SELECT * FROM cheeps")
	return cur.fetchall()

#Add a cheep
def db_add_cheep(name, cheep):
	cur = get_db().cursor()
	t = str(time.time()) #String representation of time.
	cheep_info = (name, t, cheep)
	cur.execute("INSERT INTO cheeps VALUES (?, ?, ?)", cheep_info)
	get_db().commit()

@app.route("/")
def hello():
    cheeps = db_read_cheeps()
    print(cheeps)
    return render_template('index.html', cheeps=cheeps)

@app.route("/api/cheep", methods=["POST"])
def recieve_cheep():
	print(request.form)
	db_add_cheep(request.form["name"], request.form["cheep"])
	return redirect("/")

if __name__ == "__main__":
	app.run(debug=True)