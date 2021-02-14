from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import psycopg2
import connect
import uuid

dbconn = None

app = Flask(__name__)

# this function is available for all of apps
def getCursor():
    global dbconn
    if dbconn == None:
        conn = psycopg2.connect(dbname=connect.dbname, user=connect.dbuser, password=connect.dbpass, host=connect.dbhost, port=connect.dbport)
        conn.autocommit = True
        dbconn = conn.cursor()
        return dbconn
    else:
        return dbconn


def genID():
    return uuid.uuid4().fields[1]


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/members")
def members():
    cur = getCursor()
    cur.execute("SELECT memberid, familyname, firstname from member;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('memberresult.html',dbresult=select_result,dbcols=column_names)


@app.route("/memberid", methods=['GET'])
def getAMember():
    print(request.args)
    memberid = request.args.get("memberid")
    print(memberid)

    cur = getCursor()
    cur.execute("SELECT * from member where memberid=%s",(memberid,))
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('memberresult.html', dbresult=select_result,dbcols=column_names)


@app.route("/member", methods=['GET','POST'])
def getUpdateForm():
    if request.method == 'POST':
        print(request.form)
        id = genID()
        print(id)

        familyname = request.form.get("familyname")
        firstname = request.form.get("firstname")
        dateofbirth = request.form.get("dateofbirth")
        adultleader = request.form.get("adultleader")

        # getting our connection do the database
        cur = getCursor()
        cur.execute("INSERT INTO member(memberid, familyname, firstname, dateofbirth, adultleader) VALUES (%s,%s,%s,%s,%s);",(str(id),familyname,firstname,dateofbirth,adultleader,))
        cur.execute("SELECT * FROM member where memberid=%s",(str(id),))
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('memberresult.html',dbresult=select_result,dbcols=column_names)
    else:
        return render_template('updatememberform.html')


@app.route('/member/update', methods=['GET','POST'])
def memberUpdated():
    if request.method == 'POST':
            memberid = request.form.get('memberid')
            familyname = request.form.get('familyname')
            firstname = request.form.get('firstname')
            dateofbirth = request.form.get('dateofbirth')
            adultleader = request.form.get('adultleader')
            cur = getCursor()
            cur.execute("UPDATE member SET familyname=%s, firstname=%s, dateofbirth=%s, adultleader=%s where memberid=%s",(familyname,firstname,dateofbirth,adultleader, str(memberid),))
            return redirect("/members")
    else:
        id = request.args.get('memberid')
        if id == '':
            return redirect("/members")
        else:
            cur = getCursor()
            cur.execute("SELECT * FROM member where memberid=%s",(str(id),))
            select_result = cur.fetchone()
            print(select_result)
            return render_template('updatememberform.html',memberdetails=select_result)


@app.route("/adult")
def adult():
    cur = getCursor()
    cur.execute("SELECT memberid, familyname,firstname,dateofbirth,attendancestatus \
        from group_member_attendance WHERE extract(YEAR FROM dateofbirth) <= 2003;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('adultresult.html',dbresult=select_result,dbcols=column_names)


@app.route('/youth')
def youth():
    cur = getCursor()
    cur.execute("SELECT memberid, familyname,firstname,dateofbirth,attendancestatus \
        from group_member_attendance WHERE extract(YEAR FROM dateofbirth) > 2002;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('youthresult.html',dbresult=select_result,dbcols=column_names)


@app.route('/attendance/update', methods=['GET','POST'])
def attendanceUpdate():
    if request.method == 'POST':
            memberid = request.form.get('memberid')
            familyname = request.form.get('familyname')
            firstname = request.form.get('firstname')
            dateofbirth = request.form.get('dateofbirth')
            adultleader = request.form.get('adultleader')
            groupid = request.form.get('groupid')
            joindate = request.form.get('joindate')
            activitynightid = request.form.get('activitynightid')
            attendancestatus = request.form.get('attendancestatus')
            notes = request.form.get('notes')


            cur = getCursor()
            cur.execute("UPDATE group_member_attendance SET familyname=%s, firstname=%s, dateofbirth=%s, adultleader=%s, groupid=%s, joindate=%s, activitynightid=%s, attendancestatus=%s,notes=%s where memberid=%s",  (familyname,firstname,dateofbirth,adultleader,groupid, joindate,activitynightid,attendancestatus,notes, str(memberid),))
            return redirect("/youth")
    else:
        id = request.args.get('memberid')
        if id == '':
            return redirect("/youth")
        else:
            cur = getCursor()
            cur.execute("SELECT * FROM group_member_attendance where attendancestatus=%s",(str(id),))
            select_result = cur.fetchone()
            print(select_result)
            return render_template('youthAttendanceForm.html',memberdetails=select_result)


@app.route('/groups')
def groups():
    cur = getCursor()
    cur.execute("select groupid,groupname,description,nighttitle,starttime,endtime from groupsactivitynight;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('activityresult.html',dbresult=select_result,dbcols=column_names)