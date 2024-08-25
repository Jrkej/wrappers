#by jrke(Akshat Srivastava)
from flask import Flask, render_template,request,redirect,url_for
import datetime
import mysql.connector as mysql
from hashlib import sha256
import requests


app = Flask(__name__)

#some constants
databaseName = "wrappers"
passkey = "Akshat*1c++sql"
semester = "Autumn"
session = "2024-25"
keys = {'thomso': '4405de62e2d2b354ce7b4c5cd33cbcd02a1b59866d08fb6d84a162104ce33a73', 'cinesec': 'bbcf9cb7138beb3732ecf25c1f5441a552ed78a4c2e179ef6e8b3ba3d0ff864d', 'comedy club': '8170d962605cae7c1a29106ea8b28de1591852d25ffc3cfe10fbfe5db54b85f5', 'Ecell': '0a04f26be9bc0e52ec52c83323383c5c4335d4cd8c202dabda11c21ebbddc51e', 'kshitij': '659571c90d77cbaece4d5674d5609cc7a104002d57cfbb8f3b9270b30ad114ac', 'music club': 'bbbe030df4a0775589ecd0f6933c0efa93a7aae69c70a795126c7669c24df32c', 'chess club': 'b5e9f69f1ae3a1347090ad53ab75a4edd459b9407502015ae5101e8440d07a4c'}

"""
    The given site shows the schedule of lectures + events organised by clubs/commitee etc etc
    for lecture data -- scrapper is made to scrape data from site
    currently data is saved in mysql(localdatabase)
    further scope - weekly table, security for a student, delete and update of event/lectures, holiday updates
"""

def eventsave(Club,Event,Date,Time,Venue):
    """
        saves the event data in the database in the table named event
    """
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("insert into event values('{}','{}','{}','{}','{}')".format(Club,Event,Date,Time,Venue))
    cur.execute("commit")
    con.close()

def classave(Name, Course, Day, Time, Venue, factulty, enroll):
    """
        saves the information of lectures in table named lecture
    """
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("insert into lecture values('{}','{}','{}','{}','{}','{}','{}')".format(Name, Course, Day, Time, Venue, factulty, enroll))
    cur.execute("commit")
    con.close()

def getevents(Date):
    """
        returns a list of all events occuring on given date
    """
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("select * from event where Date ='"+Date+"'")
    event=cur.fetchall()
    con.close()
    return event

def getlectures(Name, Day):
    """
        returns the list of lectures of given student name, day
    """
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("select distinct * from lecture where name='"+Name+"' and Day='"+Day+"'")
    event=cur.fetchall()
    con.close()
    if len(event) == 0:
        con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
        cur=con.cursor()
        cur.execute("select distinct * from lecture where name='"+Name+"'")
        event=cur.fetchall()
        con.close()
        if len(event) == 0:
            return []
        return event[0][-1]
    return event

def creatorevent():
    """
        creates the table event
    """
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("create table event(Club char(25),Event char(25),Date date,Time char(10),Venue char(25));")
    cur.execute("commit")
    con.close()

def creatorlectures():
    """
        creates the table lecture
    """
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("create table lecture(Name char(25),Course char(30),Day char(12),Time char(10),Venue char(25),Faculty char(50), Enroll int);")
    cur.execute("commit")
    con.close()  

def createDatabase():
    """
        creates the database wrappers
    """
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey)
    cur=con.cursor()
    cur.execute(f"create database {databaseName};")
    cur.execute("commit")
    con.close()

def getTimeTable(enroll, subBatch):
    """
        this is the scrapper made to fetch details of all lectures of given enrollment number and sub batch and return it as a list
    """
    courses = requests.post("https://timetable.iitr.ac.in:4400/api/external/studentscourse", data={"EnrollmentNo":enroll, "Semester":semester, "StSessionYear":session}).json()["result"]
    courseMeta = []
    i = 0
    coursesNames = {}
    for course in courses:
        curr = {
            "Course_code":course["SubjectCode"],
            "name":course["SubjectName"],
            "SubjectArea":course["SubjectArea"],
            "Program_id":course["ProgramID"],
            "Semester":semester,
            "Session":course["StSessionYear"],
            "years":course["SemesterID"]
        }
        coursesNames[course["SubjectCode"]] = course["SubjectName"]
        courseMeta.append(curr)
        i += 1
    c = []
    classes =requests.post("https://timetable.iitr.ac.in:4400/api/aao/dep/lecturecoursbatch", json=courseMeta).json()["result"]
    for i in classes:
        try:
            if subBatch in i['Sub_Batches']:
                c.append({"time":i['Time'], "course":f"{coursesNames[i['Course_code']][:20]}({i['Course_code']})", "day":i['Day'], "venue":i['Room_no'], "fac":i['Faculty_name']})
        except:
            pass
    tuts = requests.post("https://timetable.iitr.ac.in:4400/get/studentsNo/studentcoursetut", data={"Semester":semester, "Session":session, "semid":courseMeta[0]['years'], "SubBatch":subBatch, "Branch_Name":courseMeta[0]["Program_id"]}).json()["result"]
    for i in tuts:
        try:
            c.append({"time":i['Time'], "day":i['Day'], 'course':f"{coursesNames[i['subjectAlphaCode']][:20]}({i['subjectAlphaCode']})", "venue":i['LHall'], "fac":i['FacultyName']})
        except:
            pass
    return c

def save(name, enroll, sub):
    """
        driver function of scrapper and also saves the data
    """
    classes = getTimeTable(enroll, sub)
    for i in classes:
        classave(name, i['course'], i['day'], i['time'].split('-')[0], i['venue'], i['fac'][:50], enroll)

def create():
    """
        driver for creating tables and databases,
        uses try and except, so that in case tables are present then it doesn't throw an error
    """
    try:
        createDatabase()
    except:
        pass

    try:
        creatorevent()
    except:
        pass

    try:
        creatorlectures()
    except:
        pass

def getData(name, date):
    """
        returns the list of events and lectures for a student on given date and name
    """
    splits = date.split('-')
    day = datetime.datetime(int(splits[0]), int(splits[1]), int(splits[2])).strftime("%A")
    eventdata = getevents(date)
    classdata = getlectures(name, day)
    table = []
    enroll = ""
    if type(classdata) == int:
        enroll = classdata
    else:
        for lecture in classdata:
            curr = [lecture[3], lecture[1], lecture[5], lecture[4]]
            table.append(curr)
            enroll = lecture[6]
    for event in eventdata:
        curr = [event[3], event[1], event[0], event[4]]
        table.append(curr)
    table.sort(key = lambda a:a[0])
    data = {"name": name, "date":date, "day":day, "entries":table, "enroll":enroll}
    return data

@app.route("/",methods=["GET", "POST"])
def home():
    #home page
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        return redirect(f"/timetable/{request.form['name']}/{datetime.datetime.now().date()}")
    else:
        return "INCORRECT METHOD"

@app.route("/event",methods=["GET", "POST"])
def events():
    #adding events page
    if request.method == "GET":
        return render_template("clubs.html")
    elif request.method == "POST":
        print(request.form)
        if sha256(bytes(request.form['key'], "utf-8")).hexdigest() == keys[request.form['club']]:#for security
            eventsave(request.form['club'], request.form['event'], request.form['date'], request.form['time'], request.form['venue'])
        return redirect(url_for("home"))
    else:
        return "INCORRECT METHOD"

@app.route("/lecture",methods=["GET", "POST"])
def lecture():
    #adding lectures page
    if request.method == "GET":
        return render_template("classes.html")
    elif request.method == "POST":
        save(request.form['name'], request.form['enroll'], request.form['sub'].upper())
        return redirect(url_for("home"))
    else:
        return "INCORRECT METHOD"

@app.route("/timetable/<name>/<date>",methods=["GET", "POST"])
def timetable(name, date):
    #showing the timetable page
    if request.method == "GET":
        data = getData(name, date)
        return render_template("table.html", data=data)
    elif request.method == "POST":
        print("HERE")
        return redirect(f"/timetable/{name}/{request.form['date']}")
    else:
        return "INCORRECT METHOD"

if __name__ == "__main__":
    print("CREATED BY AKSHAT, VANSH AND ARYAN")
    create()
    app.run()