from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import flash
import re

app = Flask(__name__)
app.secret_key = "super secret key"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# username is root
# password is database pwd
# localhost is ip address (of instance)
# db_name is db name (db3 for example)

db = SQLAlchemy(app)
class person(db.Model):
    id = db.Column('person_id', db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))  
    time_zone_name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, id, first_name, last_name, time_zone_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.time_zone_name = time_zone_name
        self.email = email

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    #To create/use the database mentioned in the URI
   db.create_all()
   app.run(debug = True)

@app.route("/attendee/", methods = ['GET', 'POST'])
def attendee():
    if request.method == 'POST':
        if not request.form['first_name'] or not request.form['last_name'] or not request.form['time_zone_name'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
            pers = person(25, request.form['first_name'], request.form['last_name'], request.form['time_zone_name'], request.form['email'])
        
            db.session.add(pers)
            db.session.commit()
         
            flash('Record was successfully added')
            #return redirect(url_for('show_all'))
    return render_template("attendee.html")

@app.route("/ranking/")
def ranking():
    return render_template("ranking.html", person = person.query.all())

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
