from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import flash
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = "super secret key"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@35.232.209.150/mydb'
# username is root
# password is database pwd
# localhost is ip address (of instance)
# db_name is db name (db3 for example)

meeting_number_ranking = 1

db = SQLAlchemy(app)
class person(db.Model):
    id = db.Column('person_id', db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))  
    time_zone_name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, first_name, last_name, time_zone_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.time_zone_name = time_zone_name
        self.email = email

class time_zone(db.Model):
    tname = db.Column('name', db.String(50), primary_key = True)
    offset = db.Column(db.Integer)

    def __init__(self, tname, offset):
        self.tname = tname
        self.offset = offset

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    #To create/use the database mentioned in the URI
   db.create_all()
   app.run(debug = True)

@app.route("/newAttendee/", methods = ['GET', 'POST'])
def newAttendee():
    if request.method == 'POST':
        if not request.form['first_name'] or not request.form['last_name'] or not request.form['time_zone_name'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
            pers = person(request.form['first_name'], request.form['last_name'], request.form['time_zone_name'], request.form['email'])
        
            db.session.add(pers)
            db.session.commit()
         
            flash('Record was successfully added')
            #return redirect(url_for('show_all'))
    return render_template("newAttendee.html", tzones = time_zone.query.all())

@app.route("/newCreator/", methods = ['GET', 'POST'])
def newCreator():
    if request.method == 'POST':
        if not request.form['first_name'] or not request.form['last_name'] or not request.form['time_zone_name'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
            pers = person(request.form['first_name'], request.form['last_name'], request.form['time_zone_name'], request.form['email'])
        
            db.session.add(pers)
            db.session.commit()
         
            flash('Record was successfully added')
            #return redirect(url_for('show_all'))
   
    return render_template("newCreator.html", tzones = time_zone.query.all())

@app.route("/ranking/")
def ranking():
    cnx = mysql.connector.connect(user="root", password="123456", host="35.232.209.150", database="mydb")
    cursor = cnx.cursor()
    try:
        query = """
                select date, start_time, end_time, count(person_id) as people_available 
                from 
                    (select link_meeting.availability_id, person.person_id, date, start_time, end_time from availability_info, person, link_meeting where link_meeting.person_id = person.person_id and link_meeting.availability_id = availability_info.availability_id and link_meeting.meeting_id = '{}') 
                    as table_times 
                group by availability_id 
                order by people_available desc;""".format(meeting_number_ranking)
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err)
    
    data = cursor.fetchall()
    cursor.close()
    cnx.close()

    cnx2 = mysql.connector.connect(user="root", password="123456", host="35.232.209.150", database="mydb")
    cursor2 = cnx2.cursor()
    try:
        query2 = """
            select availability_id, level_1, level_2, level_3, level_4, level_5, (level_1 + level_2 + level_3 + level_4 + level_5) as total, date, start_time, end_time

            from 
                (select availability_id, sum(importance_level = 1) as level_1, sum(importance_level = 2) as level_2, sum(importance_level = 3) as level_3, sum(importance_level = 4) as level_4, sum(importance_level = 5) as level_5, date, start_time, end_time
                from 
                    (select link_meeting.meeting_id, link_meeting.availability_id, person.person_id, importance.importance_level, date, start_time, end_time

                    from availability_info, person, link_meeting, importance, attendee_info

                    where link_meeting.person_id = person.person_id 
                    and link_meeting.availability_id = availability_info.availability_id 
                    and link_meeting.person_id = attendee_info.person_id 
                    and attendee_info.meeting_id = link_meeting.meeting_id 
                    and link_meeting.meeting_id = '{}'
                    and importance.meeting_role = attendee_info.meeting_role) as tables

                group by availability_id
                order by level_1 desc, level_2 desc, level_3 desc, level_4 desc, level_5 desc) as level_times;""".format(meeting_number_ranking)
        cursor2.execute(query2)
    except mysql.connector.Error as err:
        print(err)
    
    data2 = cursor2.fetchall()
    cursor2.close()
    cnx2.close()

    return render_template('ranking.html', data=data, data2=data2)

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
