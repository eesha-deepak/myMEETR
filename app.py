from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import flash
from flask import redirect, render_template, url_for
from flask import redirect, render_template, url_for
import mysql.connector
import re
import sqlalchemy


app = Flask(__name__)
app.secret_key = "super secret key"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@34.94.231.54/db1'
# password is database pwd
# localhost is ip address (of instance)
# db_name is db name (db3 for example)

meeting_id_ranking = 1
meeting_id_attendee = 1

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

class importance(db.Model):
    role = db.Column('meeting_role', db.String(50), primary_key = True)
    importance_level = db.Column(db.Integer)

    def __init__(self, iname, offset):
        self.role = role
        self.importance_level = importance_level

class link_meeting(db.Model):
    availability_id = db.Column('availability_id', db.Integer, primary_key = True)
    meeting_id = db.Column('meeting_id', db.Integer, primary_key = True)
    person_id = db.Column('person_id', db.Integer, primary_key = True)

    def __init__(self, tname, offset):
        self.availability_id = availability_id
        self.meeting_id = meeting_id
        self.person_id = person_id

class meeting_details(db.Model):
    meeting_id = db.Column('meeting_id', db.Integer, primary_key = True)


    def __init__(self, tname, offset):
        self.meeting_id = ameeting_id


@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        #get welcome page variables
        meeting_id = request.form['meeting_id']
        meeting_id_attendee = meeting_id

        A_email = request.form['A_email']
        M_email = request.form['M_email']

        R_meeting_id = request.form['R_meeting_id']
        meeting_id_ranking = R_meeting_id

        #attendee details entered
        if meeting_id and A_email and not M_email and not R_meeting_id:
            #check if attendee email exists
            pexists = db.session.query(db.exists().where(person.email == A_email)).scalar()
            #check if attendee meeting_id exists
            mexists = db.session.query(db.exists().where(meeting_details.meeting_id == meeting_id)).scalar()

            #meeting_id exists and attendee does not exist = redirect to newAttendee page
            if(mexists and not pexists):
                return redirect(url_for('newAttendee'))

            #meeting exists for attendee = redirect to attendee page
            if (mexists and pexists):
                return redirect(url_for('availability'))

            #meeting_id and/or attendee was entered incorrectly
            else:
                flash("either meeting_id or email was entered incorrectly")
                return render_template('welcome.html')
        
        #creator details entered
        if not meeting_id and not A_email and not R_meeting_id and M_email:
            #check if meeting_id exists
            mexists = db.session.query(db.exists().where(meeting_details.meeting_id == meeting_id)).scalar()

            #if meeting_id exists = redirect to creator enter meeting details page
            if mexists:
                flash('redirect to creator dashboard page')
                #return redirect(url_for('CREATE MEETING'))
            
            #if meeting_id does not exist = redirect to new creator page
            else:
                flash('redirect to new creator page')
                #return redirect(url_for('NEW CREATOR PAGE'))

        #if get ranking details filled
        if not meeting_id and not A_email and not M_email and R_meeting_id:
            #check in meeting_id exists
            mexists = db.session.query(db.exists().where(meeting_details.meeting_id == R_meeting_id)).scalar()

            #if meeting_id exists = redirect to ranking page
            if mexists:
                return redirect(url_for('ranking'))

            #if meeting_id does not exists = error
            else:
                flash('incorrect meeting id for  ranking')
                return render_template('welcome.html')
        
        #all the fields were empty
        elif not meeting_id and not A_email and not M_email:
            flash('nothing was entered, all fields are blank')
            return render_template('welcome.html')
        
        #lol in case some happens eekie
        else:
            return render_template('welcome.html')
    else: 
        return render_template('welcome.html')

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

@app.route("/availability/", methods = ['GET', 'POST'])
def availability():
    if request.method == 'POST':
        if not request.form['start_time'] or not request.form['end_time'] or not request.form['importance_name'] or not request.form['year'] or not request.form['month'] or not request.form['date']:
            flash('Please enter all the fields', 'error')
        else:
            # do all my checky checks
            stime = request.form['start_time']
            etime = request.form['end_time'] 
         
    return render_template("availability.html", implevels = importance.query.all())

@app.route("/ranking/")
def ranking():
    cnx = mysql.connector.connect(user="root", password="12345", host="34.94.231.54", database="db1")
    cursor = cnx.cursor(prepared=True)
    try:
        query = """
                select date, start_time, end_time, count(person_id) as people_available 
                from 
                    (select link_meeting.availability_id, person.person_id, date, start_time, end_time from availability_info, person, link_meeting where link_meeting.person_id = person.person_id and link_meeting.availability_id = availability_info.availability_id and link_meeting.meeting_id = %s) 
                    as table_times 
                group by availability_id 
                order by people_available desc;"""
        cursor.execute(query, (meeting_id_ranking, ))
    except mysql.connector.Error as err:
        print(err)
    
    data = cursor.fetchall()
    cursor.close()
    cnx.close()

    cnx2 = mysql.connector.connect(user="root", password="12345", host="34.94.231.54", database="db1")
    cursor2 = cnx2.cursor(prepared=True)
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
                    and link_meeting.meeting_id = %s
                    and importance.meeting_role = attendee_info.meeting_role) as tables
                group by availability_id
                order by level_1 desc, level_2 desc, level_3 desc, level_4 desc, level_5 desc) as level_times;"""
        cursor2.execute(query2, (meeting_id_ranking, ))
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
