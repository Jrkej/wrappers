from flask import Flask, render_template,request,redirect,url_for
import datetime
import mysql.connector as mysql
from hashlib import sha256
import requests


app = Flask(__name__)

databaseName = "wrappers"
passkey = "Akshat*1c++sql"
semester = "Autumn"
session = "2024-25"
keys = {"a":sha256(b"abc").hexdigest()}

def eventsave(Club,Event,Date,Time,Venue):
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("insert into event values('{}','{}','{}','{}','{}')".format(Club,Event,Date,Time,Venue))
    cur.execute("commit")
    con.close()

def classave(Name, Course, Day, Time, Venue, factulty):
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("insert into lecture values('{}','{}','{}','{}','{}', '{}')".format(Name, Course, Day, Time, Venue, factulty))
    cur.execute("commit")
    con.close()

def getevents(Date):
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
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("select * from lecture where name='"+Name+"' and Day='"+Day+"'")
    event=cur.fetchall()
    con.close()
    return event

def creatorevent():
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("create table event(Club char(25),Event char(25),Date date,Time char(10),Venue char(25));")
    cur.execute("commit")
    con.close()

def creatorlectures():
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey,
                      database=databaseName)
    cur=con.cursor()
    cur.execute("create table lecture(Name char(25),Course char(30),Day char(12),Time char(10),Venue char(25),Faculty char(50));")
    cur.execute("commit")
    con.close()  

def createDatabase():
    con=mysql.connect(host="localhost",
                      user="root",
                      password=passkey)
    cur=con.cursor()
    cur.execute(f"create database {databaseName};")
    cur.execute("commit")
    con.close()

def getTimeTable(enroll, subBatch):
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
    classes = getTimeTable(enroll, sub)
    for i in classes:
        classave(name, i['course'], i['day'], i['time'].split('-')[0], i['venue'], i['fac'][:50])

def create():
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
    splits = date.split('-')
    day = datetime.datetime(int(splits[0]), int(splits[1]), int(splits[2])).strftime("%A")
    eventdata = getevents(date)
    classdata = getlectures(name, day)
    table = []

    for lecture in classdata:
        curr = [lecture[3], lecture[1], lecture[5], lecture[4]]
        table.append(curr)
    for event in eventdata:
        curr = [event[3], event[1], event[0], event[4]]
        table.append(curr)
    table.sort(key = lambda a:a[0])
    data = {"name": name, "date":date, "day":day, "entries":table}
    return data

@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        return redirect(f"/timetable/{request.form['name']}/{datetime.datetime.now().date()}")
    else:
        return "INCORRECT METHOD"

@app.route("/event",methods=["GET", "POST"])
def events():
    if request.method == "GET":
        return render_template("clubs.html")
    elif request.method == "POST":
        print(request.form)
        if sha256(bytes(request.form['key'], "utf-8")).hexdigest() == keys[request.form['club']]:
            eventsave(request.form['club'], request.form['event'], request.form['date'], request.form['time'], request.form['venue'])
        return redirect(url_for("home"))
    else:
        return "INCORRECT METHOD"

@app.route("/lecture",methods=["GET", "POST"])
def lecture():
    if request.method == "GET":
        return render_template("classes.html")
    elif request.method == "POST":
        save(request.form['name'], request.form['enroll'], request.form['sub'])
        return redirect(url_for("home"))
    else:
        return "INCORRECT METHOD"

@app.route("/timetable/<name>/<date>",methods=["GET", "POST"])
def timetable(name, date):
    if request.method == "GET":
        data = getData(name, date)
        return render_template("table.html", data=data)
    elif request.method == "POST":
        print("HERE")
        return redirect(f"/timetable/{name}/{request.form['date']}")
    else:
        return "INCORRECT METHOD"

if __name__ == "__main__":
    create()
    app.run()