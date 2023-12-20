from flask import Flask, render_template, redirect, url_for, request,\
     send_from_directory
#from werkzeug.utils import secure_filename
#import os.path

app = Flask(__name__)

import os
import sqlite3

curr_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(curr_dir, "lostandfound4.db")

#ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
#file_dir = os.path.dirname(os.path.abspath(__file__))
#UPLOAD_FOLDER = os.path.join(file_dir, 'static\\images')

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin_sign_in/", methods=["GET", "POST"])
def admin_sign_in():
    if request.method == "GET":
        return render_template("admin_sign_in.html")
    else:
        adminid = request.form["admin_id"]
        adminpw = request.form["admin_pw"]

        query = '''
SELECT Admin.AdminID, Admin.AdminPW FROM Admin WHERE
Admin.AdminID = ?'''
        db = sqlite3.connect(db_file)
        cursor = db.execute(query, (adminid,))
        records = cursor.fetchall()
        #[('Adm001', 'admin1@RVHS')]

        for eachrec in records:
            if eachrec[0] == adminid and eachrec[1] == adminpw:
                cursor.close()
                db.close()
                query = '''SELECT * FROM Item'''
                db = sqlite3.connect(db_file)
                cursor = db.execute(query)
                itemrecords = cursor.fetchall()
                #[(),()]
                cursor.close()
                db.close()

                query2 = '''SELECT * FROM Claims'''
                db = sqlite3.connect(db_file)
                cursor = db.execute(query2)
                claimsrecords = cursor.fetchall()
                #[(),()]
                cursor.close()
                db.close()
                return render_template("admin_welcome.html", adminid=adminid,
                                       itemrecords=itemrecords,
                                       claimsrecords=claimsrecords)
        cursor.close()
        db.close()
        return render_template("admin_sign_in.html")

@app.route("/admin_update/", methods=["GET", "POST"])
def admin_update():
    if request.method == "GET":
        return render_template("admin_update.html")
    else:
        adminname = request.form["admin_name"]
        itemno = request.form["item_no"]
        itemclaimer = request.form["item_claimer"]
        itemstatus = request.form["status"]
        query = '''
SELECT Item.ItemStatus FROM Item WHERE Item.ItemNo = ?'''
        db = sqlite3.connect(db_file)
        cursor = db.execute(query, (itemno,))
        curr_itemstatus = cursor.fetchone()[0]
        print(curr_itemstatus)
        cursor.close()
        db.close()
        
        query2 = '''UPDATE Item SET AdminAttendee = ?,
ItemClaimer = ?, ItemStatus = ? WHERE ItemNo = ?'''
        
        query3 = '''UPDATE Claims SET AdminAttendee = ? WHERE ItemNo = ?'''
        
        
        if str(curr_itemstatus) == "U":
            db = sqlite3.connect(db_file)
            db.execute(query2, (adminname, itemclaimer,
                                itemstatus, itemno,))
            db.commit()
            db.close()

            db = sqlite3.connect(db_file)
            db.execute(query3, (adminname, itemno,))
            db.commit()
            db.close()
            return render_template("admin_update_result.html")
        return render_template("admin_update.html")


@app.route("/user_sign_up/", methods=["GET", "POST"])
def user_sign_up():
    if request.method == "GET":
        return render_template("user_sign_up.html")
    else:
        userid = request.form["user_id"]
        username = request.form["user_name"]
        userclass = request.form["user_class"]
        userindex = request.form["user_ind"]
        useryear = request.form["user_year"]
        userpw = request.form["user_pw"]
        userpwc = request.form["user_pw_c"]
        query = '''
INSERT INTO User (UserID, UserFullname, UserClass, UserIndexNo,
YearOfSignUp, UserPW, ConfirmPW) VALUES (?,?,?,?,?,?,?)'''
        db = sqlite3.connect(db_file)
        db.execute(query, (userid, username, userclass, userindex,
                                    useryear, userpw, userpwc,))

        if userpw == userpwc:
            db.commit()
            db.close()
            query = '''SELECT * FROM Item'''
            db = sqlite3.connect(db_file)
            cursor = db.execute(query)
            itemrecords = cursor.fetchall()
            #[(),()]
            cursor.close()
            db.close()
            return render_template("user_welcome.html", userid=userid,
                                   itemrecords=itemrecords)
        else:
            db.close()
            return render_template("user_sign_up.html")
        
@app.route("/user_sign_in/", methods=["GET", "POST"])
def user_sign_in():
    if request.method == "GET":
        return render_template("user_sign_in.html")
    else:
        userid = request.form["user_id"]
        userpw = request.form["user_pw"]

        query = '''
SELECT User.UserID, User.UserPW FROM User WHERE
User.UserID = ?'''
        db = sqlite3.connect(db_file)
        cursor = db.execute(query, (userid,))
        records = cursor.fetchall()
        print(records)
        for eachrec in records:
            if eachrec[0] == userid and eachrec[1] == userpw:
                cursor.close()
                db.close()
                query = '''SELECT * FROM Item'''
                db = sqlite3.connect(db_file)
                cursor = db.execute(query)
                itemrecords = cursor.fetchall()
                #[(),()]
                cursor.close()
                db.close()
                return render_template("user_welcome.html", userid=userid,
                                       itemrecords=itemrecords)
        cursor.close()
        db.close()
        return render_template("user_sign_in.html")

@app.route("/user_welcome/")
def user_welcome():
    query = '''SELECT * FROM Item'''
    db = sqlite3.connect(db_file)
    cursor = db.execute(query)
    itemrecords = cursor.fetchall()
    #[(),()]
    cursor.close()
    db.close()
    return render_template("user_welcome.html", itemrecords=itemrecords)    

@app.route("/user_report/", methods=["GET", "POST"])
def user_report():
    if request.method == "GET":
        return render_template("user_report.html")
    else:
        itemdatef = request.form["item_date_f"]
        itemtimef = request.form["item_time_f"]
        itemloc = request.form["item_location"]
        itemfounder = request.form["item_founder"]
        itemcat = request.form["item_cat"]
        itemname = request.form["item_name"]
        itemimageurl = request.form["item_image_url"]
        
        query = '''INSERT INTO Item (ItemDateFound, ItemTimeFound,
ItemLocationFound, ItemFounder, ItemCategory, ItemName, ItemImage,
ItemStatus) VALUES (?,?,?,?,?,?,?,?)'''
        db = sqlite3.connect(db_file)
        db.execute(query, (itemdatef, itemtimef, itemloc, itemfounder,
                           itemcat, itemname, itemimageurl, "U",))
        db.commit()
        db.close()
        return render_template("user_report_result.html")
            

@app.route("/user_request/", methods=["GET", "POST"])
#problem: cannot redirect to individually claim this particular item for now
def user_request():
    if request.method == "GET":
        return render_template("user_request.html")
    else:
        itemno = request.form["item_no"]
        userid = request.form["user_id"]
        userclass = request.form["user_class"]
        userind = request.form["user_ind"]
        meetdate = request.form["meet_date"]
        meettime = request.form["meet_time"]
        meetmsg = request.form["meet_msg"]

        query = '''
    INSERT INTO Claims (ItemNo, UserID, UserClass, UserIndexNo, MeetingDate,
    MeetingTime, MeetingMsg) VALUES (?,?,?,?,?,?,?)'''
        
        query2 = '''
    SELECT Item.ItemStatus FROM Item WHERE Item.ItemNo = ?'''
        db = sqlite3.connect(db_file)
        cursor = db.execute(query2, (itemno,))
        curr_status = cursor.fetchone()[0]
        cursor.close()
        db.close()
        print(curr_status)

        if curr_status == "U":
            db = sqlite3.connect(db_file)
            db.execute(query, (itemno, userid, userclass, userind, meetdate,
                           meettime, meetmsg,))
            db.commit()
            db.close()
            return render_template("user_request_result.html")
        
        return render_template("user_request.html")
    

if __name__ == "__main__":
    app.run()

