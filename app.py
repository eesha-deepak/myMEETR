from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask import request
from flask import flash
from flask import redirect, render_template, url_for
import mysql.connector
import re
import sqlalchemy
from sqlalchemy import join
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey, Numeric, SmallInteger, DATE
import math
import decimal
import datetime
from dateutil.parser import parse
import config #stores passwords and database credentials

app = Flask(__name__)
app.secret_key = config.secret_key
app.config ['SQLALCHEMY_DATABASE_URI'] = config.db_uri

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

class availability_info(db.Model):
    id = db.Column('availability_id', db.Integer, primary_key = True)
    date = db.Column(db.String(50))
    start_time = db.Column(db.String(50))  
    end_time = db.Column(db.String(50))

    def __init__(self, date, start_time, end_time):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

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
    person_id = db.Column('person_id', db.Integer, primary_key = True)
    meeting_id = db.Column('meeting_id', db.Integer, primary_key = True)

    def __init__(self, availability_id, person_id, meeting_id):
        self.availability_id = availability_id
        self.person_id = person_id
        self.meeting_id = meeting_id

class attendee_info(db.Model):
    person_id = db.Column('person_id', db.Integer, primary_key = True)
    meeting_id = db.Column('meeting_id', db.Integer, primary_key = True)
    role = db.Column('meeting_role', db.String(50), primary_key = True)

    def __init__(self, person_id, meeting_id, role):
        self.person_id = person_id
        self.meeting_id = meeting_id
        self.role = role

class meeting_details(db.Model):
    meeting_id = db.Column('meeting_id', db.Integer, primary_key = True)
    in_person = db.Column('in_person', db.Integer)
    online = db.Column('online', db.Integer)
    start_day = db.Column('start_day', db.DATE)
    end_day = db.Column('end_day', db.DATE)
    length_hr = db.Column('length_hr', Numeric)
    description = db.Column('description', db.String(200))
    creator_id = db.Column('creator_id', db.Integer)

    def __init__(self, in_person, online, start_day, end_day, length_hr, description,creator_id):
        self.in_person = in_person
        self.online = online
        self.start_day = start_day
        self.end_day = end_day
        self.length_hr = length_hr
        self.description = description
        self.creator_id = creator_id

#will need to get from "Creator: enter details page"
global creator_meeting_id


if __name__ == '__main__':
    #To create/use the database mentioned in the URI
   db.create_all()
   app.run(debug = True)
   
@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        #get welcome page variables
        global meeting_id 
        meeting_id = request.form['meeting_id']

        global A_email
        A_email = request.form['A_email']

        global M_email
        M_email = request.form['M_email']

        global R_meeting_id
        R_meeting_id = request.form['R_meeting_id']

        #attendee details entered
        if meeting_id and A_email and not M_email and not R_meeting_id:
            #check if attendee email exists
            pexists = db.session.query(db.exists().where(person.email == A_email)).scalar()

            #check if attendee meeting_id exists
            mexists = db.session.query(db.exists().where(meeting_details.meeting_id == meeting_id)).scalar()

            #meeting_id exists and attendee does not exist = redirect to newAttendee page
            if (mexists and not pexists):
                return redirect(url_for('newAttendee'))

            #meeting exists for attendee = redirect to attendee page
            elif (mexists and pexists):
                return redirect(url_for('availability'))

            #meeting_id and/or attendee was entered incorrectly
            else:
                flash("either meeting_id or email was entered incorrectly")
                return render_template('welcome.html')
        
        #creator details entered
        if not meeting_id and not A_email and not R_meeting_id and M_email:
            #check if creator exists
            cnx = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
            cursor = cnx.cursor(prepared=True)
            query = """
                SELECT p.email
                FROM person p 
	                JOIN meeting_details m ON p.person_id = m.creator_id
                WHERE p.email = %s
                LIMIT 1;"""
            cursor.execute(query, (M_email, ))
            mexists = cursor.fetchall()
            cursor.close()
            cnx.close()

            pexists = db.session.query(db.exists().where(person.email == M_email)).scalar()

            global creator_id

            #if email for meeting creator doesn't exist BUT an attendee does exist = redirect to creator enter meeting details page
            if (not mexists and pexists):
                mci = db.session.query(person.id).filter(person.email == M_email).first()
                creator_id = mci[0]
                #redirect to creator new meeting page
                return redirect(url_for('creatorMeeting'))
            #if email for meeting creator exists BUT an attendee NOT does not exist = redirect to creator enter meeting details page    
            elif mexists:
                mci = db.session.query(person.id).filter(person.email == M_email).first()
                creator_id = mci[0]
                flash('redirect to creator dashboard page')
                #redirect to creator dashboard page
                #return redirect(url_for('CREATOR DASHBOARD PAGE'))
                return render_template('welcome.html')           
            #if email for meeting creator or attendee does not exist and 
            else:
                #redirect to new creator page
                return redirect(url_for('newCreator'))

        #if get ranking details filled
        if not meeting_id and not A_email and not M_email and R_meeting_id:
            #check in meeting_id exists
            mexists = db.session.query(db.exists().where(meeting_details.meeting_id == R_meeting_id)).scalar()

            #if meeting_id exists = redirect to ranking page
            if mexists:
                return redirect(url_for('ranking'))

            #if meeting_id does not exists = error
            else:
                flash('incorrect meeting id for ranking')
                return render_template('welcome.html')
        
        #all the fields were empty
        if not meeting_id and not A_email and not M_email:
            flash('nothing was entered, all fields are blank')
            return render_template('welcome.html')
        
        #lol in case some happens eekie
        else:
            flash('some weird error, try again')
            return render_template('welcome.html')
    else: 
        return render_template('welcome.html')

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

@app.route("/availability/", methods = ['GET', 'POST'])
def availability():
    if request.method == 'POST':
        # check to make sure all the values were filled
        if not request.form['start_time'] or not request.form['end_time'] or not request.form['importance_name'] or not request.form['year'] or not request.form['month'] or not request.form['date']:
            return render_template('availability.html', implevels = importance.query.all())
        else:
            # do all my error checky checks

            # first get all the values 
            a_role = request.form['importance_name']

            date = int(request.form['date'])
            year = request.form['year']
            month = request.form['month']

            # from the start time and the end time, get the hours and the minutes
            stime = request.form['start_time']
            shour = int(stime.split(':')[0])
            sminutes = int(stime.split(':')[1])

            etime = request.form['end_time']
            ehour = int(etime.split(':')[0])
            eminutes = int(etime.split(':')[1])
  
            # bool vars to check if any of these values go to the prev or the next day
            snext = False
            enext = False
            sprev = False
            eprev = False

            # get the person's id and the time_zone offset
            cnx = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
            cursor = cnx.cursor(prepared=True)
            query = """
                    select person.person_id, time_zone.offset
                    from person
                        JOIN time_zone on person.time_zone_name = time_zone.name
                    where person.email = %s;"""
            cursor.execute(query, (A_email, ))

            data = cursor.fetchall()
            cursor.close()
            cnx.close()
            attendee_id = data[0][0]
            offset = decimal.Decimal(data[0][1])

            # get the minutes and the hours of the offset
            min_frac, hour = math.modf(offset)

            # do the math for minutes, multiply the offset decimal by 60, add to the minutes, and check if the value
            # do modular math to get the right incremented value
            min_frac = min_frac * 60
            sminutes = sminutes + min_frac
            if sminutes < 0:
                shour = shour - 1
            elif sminutes >= 60:
                shour = shour + 1
            sminutes = sminutes % 60

            eminutes = eminutes + min_frac
            if eminutes < 0:
                ehour = ehour - 1
            elif eminutes >= 60:
                ehour = ehour + 1
            eminutes = eminutes % 60

            # do the math for hours, check the value
            # do modular math to increment correctly
            shour = shour + hour
            if shour < 0:
                sprev = True
            elif shour >= 24:
                snext = True
            shour = shour % 24
            
            ehour = ehour + hour
            if ehour < 0:
                eprev = True
            elif ehour >= 24:
                enext = True
            ehour = ehour % 24

            # not on the same day
            if sprev != eprev or snext != enext:
                return render_template('availability.html', implevels = importance.query.all())
            
            # get the dates and the time_block for the meeting
            cnx3 = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
            cursor3 = cnx3.cursor(prepared=True)
            query3 = """
                    select start_day, end_day, length_hr
                    from meeting_details
                    where meeting_details.meeting_id = %s;"""
            cursor3.execute(query3, (meeting_id, ))
            data3 = cursor3.fetchall()
            cursor3.close()
            cnx3.close()

            # make all of these datetime.datetime
            first_day = datetime.datetime.combine(data3[0][0], datetime.time(0, 0))
            last_day = datetime.datetime.combine(data3[0][1], datetime.time(0, 0))
            time_block = decimal.Decimal(data3[0][2])

            # increment the date based on what we calculated in the hours and minutes section
            if sprev == True:
                date = date - 1
            elif snext == True:
                date = date + 1

            full_date = year + "-" + month + "-" + str(date)
            date_obj = datetime.datetime.strptime(full_date, '%Y-%m-%d')

            # check if it is between the right days/months/years
            if first_day <= date_obj <= last_day:
                print("")
            else:
                return render_template('availability.html', implevels = importance.query.all())
            
            start_time = ""
            end_time = ""

            # get the right time printed out in the correct format
            s_string = str(sminutes) 
            length = len(s_string) 
            if length == 1:
                start_time = str(int(shour)) + ":0" + str(int(sminutes)) + ":00"
            elif sminutes == 0:
                start_time = str(int(shour)) + ":00:00"
            else:
                start_time = str(int(shour)) + ":" + str(int(sminutes)) + ":00"

            e_string = str(eminutes) 
            length = len(e_string) 
            if length == 1:
                end_time = str(int(ehour)) + ":0" + str(int(eminutes)) + ":00"
            elif eminutes == 0:
                end_time = str(int(ehour)) + ":00:00"
            else:
                end_time = str(int(ehour)) + ":" + str(int(eminutes)) + ":00"
            
            FMT = '%H:%M:%S'
            tdelta = datetime.datetime.strptime(end_time, FMT) - datetime.datetime.strptime(start_time, FMT)
            dhour = int(str(tdelta).split(':')[0])
            dminutes = int(str(tdelta).split(':')[1])

            d_min_to_hour = dminutes/60
            delta_time = dhour + d_min_to_hour

            # number of hours and minutes is wrong compared to the one provided from the meeting
            if delta_time != time_block:
                return render_template('availability.html', implevels = importance.query.all())
            

            # now we finally know that the data is CORRECT!
            cnx4 = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
            cursor4 = cnx4.cursor(prepared=True)
            query4 = """
                    select availability_id
                    from availability_info
                    where availability_info.date = %s
                    and availability_info.start_time = %s
                    and availability_info.end_time = %s;"""
            cursor4.execute(query4, (full_date, start_time, end_time, ))
            data4 = cursor4.fetchall()
            cursor4.close()
            cnx4.close()

            av_id = 0
            
            if len(data4)==0:
                ai = availability_info(full_date, start_time, end_time)
                db.session.add(ai)
                db.session.commit()
                av_id = ai.id
            else:
                av_id = data4[0][0]

            cnx5 = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
            cursor5 = cnx5.cursor(prepared=True)
            query5 = """
                    select *
                    from link_meeting
                    where link_meeting.availability_id = %s
                    and link_meeting.person_id = %s
                    and link_meeting.meeting_id = %s;"""
            cursor5.execute(query5, (av_id, attendee_id, meeting_id, ))
            data5 = cursor5.fetchall()
            cursor5.close()
            cnx5.close()
            
            if len(data5)==0:
                lm = link_meeting(av_id, attendee_id, meeting_id)
                db.session.add(lm)
                db.session.commit()
            
            cnx6 = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
            cursor6 = cnx6.cursor(prepared=True)
            query6 = """
                    select *
                    from attendee_info
                    where attendee_info.person_id = %s
                    and attendee_info.meeting_id = %s;"""
            cursor6.execute(query6, (attendee_id, meeting_id, ))
            data6 = cursor6.fetchall()
            cursor6.close()
            cnx6.close()
            
            if len(data6)==0:
                ai = attendee_info(attendee_id, meeting_id, a_role)
                db.session.add(ai)
                db.session.commit()
         
    return render_template("availability.html", implevels = importance.query.all())

@app.route("/ranking/")
def ranking():
    cnx = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
    cursor = cnx.cursor(prepared=True)
    try:
        query = """
                select date, start_time, end_time, count(person_id) as people_available 
                from 
                    (select link_meeting.availability_id, person.person_id, date, start_time, end_time from availability_info, person, link_meeting where link_meeting.person_id = person.person_id and link_meeting.availability_id = availability_info.availability_id and link_meeting.meeting_id = %s) 
                    as table_times 
                group by availability_id 
                order by people_available desc;"""
        cursor.execute(query, (R_meeting_id, ))
    except mysql.connector.Error as err:
        print(err)
    
    data = cursor.fetchall()
    cursor.close()
    cnx.close()

    cnx2 = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.db)
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
        cursor2.execute(query2, (R_meeting_id, ))
    except mysql.connector.Error as err:
        print(err)
    
    data2 = cursor2.fetchall()
    cursor2.close()
    cnx2.close()

    return render_template('ranking.html', data=data, data2=data2)

@app.route("/editMeetingDetails/", methods = ['GET', 'POST'])
def editMeetingDetails():
    # inp = 1: inperson
    mode = db.session.query(meeting_details.in_person).filter(meeting_details.meeting_id == creator_meeting_id).all()
    m = mode[0][0]
    if(m == 1):
        inp = 1
        p = 'in person'
        op = 0
        o = 'online'
    else:
        inp = 0
        p = 'online'
        op = 1
        o = 'in person'

    desc = db.session.query(meeting_details.description).filter(meeting_details.meeting_id == creator_meeting_id).all()
    d = desc[0][0]

    if request.method == 'POST':
        m_mode = request.form['m_mode']
        descript = request.form['description']

        if (m_mode == '1'):
            in_person = 1
            online = 0
        else:
            in_person = 0
            online = 1


        if(descript):
            description = descript
            db.session.query(meeting_details).filter(meeting_details.meeting_id == creator_meeting_id).update(
                {'in_person':in_person, 'online':online, 'description':description, 'creator_id':creator_id})            
            db.session.commit() 
            flash('your meeting details have been updated if you made any changes')
            flash('click "HOME" in the upper left hand corner to log out')

            #return redirect(url_for('CREATOR DASHBOARD')) 
            #return redirect(url_for('home'))   
            return redirect(url_for('editMeetingDetails'))      
        elif (not descript):
            description = d
            db.session.query(meeting_details).filter(meeting_details.meeting_id == creator_meeting_id).update(
                {'in_person':in_person, 'online':online, 'description':description, 'creator_id':creator_id}) 
            db.session.commit() 
            flash('your meeting details have been updated if you made any changes')
            flash('click "HOME" in the upper left hand corner to log out')

            #return redirect(url_for('CREATOR DASHBOARD')) 
            #return redirect(url_for('home'))
            return redirect(url_for('editMeetingDetails'))
        else:
            return redirect(url_for('editMeetingDetails'))
        
    return render_template("editMeetingDetails.html", inp=inp, p=p, op=op, o=o, d=d)

@app.route("/creatorMeeting/", methods = ['GET', 'POST'])
def creatorMeeting():
    if request.method == 'POST':
        print(creator_id)
        start = request.form['start_day']
        end = request.form['end_day']
        start_day = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_day = datetime.datetime.strptime(end, '%Y-%m-%d')

        length = float(request.form['length'])

        meeting_format = request.form['inperson-online']
        inperson = -1
        online = -1
        if(meeting_format == '1'):
            inperson = 1
            online = 0

        else:
            inperson = 0
            online = 1

        if length <= 0.00:
            flash('Please enter a correct meeting length','error')

        elif start_day > end_day:
           flash('Please enter correct dates','error')

        elif request.form['inperson-online'] and request.form['length'] and request.form['meeting_description'] and request.form['start_day'] and request.form['end_day']:
            newMeeting = meeting_details(inperson, online, start_day, end_day, request.form['length'], request.form['meeting_description'], creator_id)
            db.session.add(newMeeting)
            db.session.commit()
            flash('Record was successfully added')

        elif not request.form['inperson-online'] or not request.form['length'] or not request.form['meeting_description'] or not request.form['start_day'] or not request.form['end_day']:
            flash('Please enter all the fields','error')

    return render_template("creatorMeeting.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
