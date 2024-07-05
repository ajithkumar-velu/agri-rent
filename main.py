from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="agri_rental"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        page = request.form['page']
        if page=="login":
            username1 = request.form['uname']
            password1 = request.form['pass']
            
            mycursor.execute("SELECT count(*) FROM ar_user where uname=%s && pass=%s",(username1,password1))
            myresult = mycursor.fetchone()[0]
            print(myresult)
            if myresult>0:
                session['username'] = username1
                
                return redirect(url_for('userhome')) 
            else:
                msg="no"

        elif page=="reg":
            name = request.form['name']
            address = request.form['address']
            district = request.form['district']
            mobile = request.form['mobile']
            email = request.form['email']
            uname = request.form['uname']
            pass1 = request.form['pass']

            mycursor.execute("SELECT count(*) FROM ar_user where uname=%s || email=%s",(uname,email))
            cnt = mycursor.fetchone()[0]
            if cnt==0:
                mycursor.execute("SELECT max(id)+1 FROM ar_user")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                sql = "INSERT INTO ar_user(id,name,address,district,mobile,email,uname,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,name,address,district,mobile,email,uname,pass1)
                mycursor.execute(sql, val)
                mydb.commit()
                msg="success"
            else:
                msg="fail"
            
        

    return render_template('index.html',msg=msg,act=act)

@app.route('/login_pro',methods=['POST','GET'])
def login_pro():
    cnt=0
    act=""
    msg=""

    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ar_provider where uname=%s && pass=%s && status=1",(username1,password1))
        myresult = mycursor.fetchone()[0]
        print(myresult)
        if myresult>0:
            session['username'] = username1
            
            return redirect(url_for('pro_home')) 
        else:
            msg="Invalid Username or Password! or not approved"
            
        

    return render_template('login_pro.html',msg=msg,act=act)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ar_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            return redirect(url_for('admin')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login_admin.html',msg=msg,act=act)


@app.route('/reg_pro', methods=['GET', 'POST'])
def reg_pro():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        district=request.form['district']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        account=request.form['account']
        gpay=request.form['gpay']

        

        mycursor.execute("SELECT count(*) FROM ar_provider where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM ar_provider")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO ar_provider(id,name,address,district,mobile,email,uname,pass,create_date,account,gpay) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,address,district,mobile,email,uname,pass1,rdate,account,gpay)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='fail'
            
    
    return render_template('reg_pro.html', msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get("act")
    email=""
    mess=""
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM ar_provider")
    data = mycursor.fetchall()

    if act=="ok":
        pid=request.args.get("pid")
        mycursor.execute("update ar_provider set status=1 where id=%s",(pid,))
        mydb.commit()
        msg="success"
    
    
    return render_template('admin.html',msg=msg,data=data,act=act)


@app.route('/pro_home', methods=['GET', 'POST'])
def pro_home():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    return render_template('pro_home.html',data=data,act=act)


@app.route('/pro_add', methods=['GET', 'POST'])
def pro_add():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        vehicle=request.form['vehicle']
        vno=request.form['vno']
        details=request.form['details']
        cost1=request.form['cost1']
        cost2=request.form['cost2']
        file= request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM ar_vehicle")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        if file:
            fname1 = file.filename
            fname = secure_filename(fname1)
            photo="P"+str(maxid)+fname
            file.save(os.path.join("static/upload/", photo))
                
        sql = "INSERT INTO ar_vehicle(id,uname,vehicle,vno,details,cost1,cost2,photo,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,vehicle,vno,details,cost1,cost2,photo,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        

        
    return render_template('pro_add.html',msg=msg,data=data,act=act)

@app.route('/pro_vehicle', methods=['GET', 'POST'])
def pro_vehicle():
    msg=""
    act=""
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    print(uname)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where uname=%s",(uname, ))
    dd2 = mycursor.fetchall()

    for ds2 in dd2:
        dt=[]
        dt.append(ds2[0])
        dt.append(ds2[1])
        dt.append(ds2[2])
        dt.append(ds2[3])
        dt.append(ds2[4])
        dt.append(ds2[5])
        dt.append(ds2[6])
        dt.append(ds2[7])
        dt.append(ds2[8])
        dt.append(ds2[9])
        s1="2"
        ss=""
        mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status=0",(uname, ds2[0]))
        cnt3 = mycursor.fetchone()[0]
        if cnt3>0:
            s1="1"
            ss=str(cnt3)

        print("ss="+ss)

        dt.append(ss)
        dt.append(s1)
        data2.append(dt)
        

    return render_template('pro_vehicle.html',msg=msg,data=data,act=act,data2=data2)

@app.route('/pro_request', methods=['GET', 'POST'])
def pro_request():
    msg=""
    vid=request.args.get("vid")
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    print(uname)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where id=%s",(vid, ))
    vdata = mycursor.fetchone()

    mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status<=1",(uname, vid))
    cnt3 = mycursor.fetchone()[0]

    if cnt3>0:
        st="1"
        mycursor.execute("SELECT * FROM ar_booking b, ar_user a where b.uname=a.uname && b.provider=%s && b.vid=%s && b.status<=1",(uname, vid))
        data2 = mycursor.fetchall()
        
       
    if act=="ok":
        bid=request.args.get("bid")
        mycursor.execute("update ar_booking set status=1 where id=%s", (bid,))
        mydb.commit()
        mycursor.execute("update ar_vehicle set status=1 where id=%s", (vid,))
        mydb.commit()
        msg="ok"
        
    return render_template('pro_request.html',msg=msg,data=data,act=act,data2=data2,vdata=vdata,st=st,vid=vid)



@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        search=request.form['search']
        st="1"

        gs='%'+search+'%'

        uu=[]
        mycursor.execute("SELECT * FROM ar_provider where name like %s || address like %s || district like %s",(gs,gs,gs))
        dd2 = mycursor.fetchall()
        for ds2 in dd2:
            uu.append(ds2[6])

        print(uu)
        if len(uu)>0:
            for u1 in uu:
                mycursor.execute("SELECT * FROM ar_vehicle where uname=%s && status=0",(u1,))
                dd3 = mycursor.fetchall()
                for ds3 in dd3:
                    data2.append(ds3)
                
                
        else:
            mycursor.execute("SELECT * FROM ar_vehicle where (uname like %s || vehicle like %s || vno like %s || details like %s) && status=0",(gs,gs,gs,gs))
            data2 = mycursor.fetchall()
        

    if st=="":
        mycursor.execute("SELECT * FROM ar_vehicle where status=0 order by rand() limit 0,10")
        data2 = mycursor.fetchall()
    
    return render_template('userhome.html',data=data,act=act,data2=data2)

@app.route('/book', methods=['GET', 'POST'])
def book():
    msg=""
    act=""
    uname=""
    st=""
    amt=0
    vdata=[]
    vid=request.args.get("vid")
    data2=[]
    if 'username' in session:
        uname = session['username']

    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where id=%s",(vid,))
    dd = mycursor.fetchone()
    pro=dd[1]
    cost1=dd[5]
    cost2=dd[6]
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(pro,))
    pdata = mycursor.fetchone()
    provider=pdata[6]
        

    if request.method=='POST':
        duration=request.form['duration']
        time_type=request.form['time_type']
        req_date=request.form['req_date']

        mycursor.execute("SELECT max(id)+1 FROM ar_booking")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        tt=int(duration)
        if time_type=="1":
            
            amt=cost1*tt
        else:
            amt=cost2*tt
        
        sql = "INSERT INTO ar_booking(id,uname,provider,vid,duration,time_type,req_date,status,amount,pay_st) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,provider,vid,duration,time_type,req_date,'0',amt,'0')
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        
    mycursor.execute("SELECT * FROM ar_booking where vid=%s",(vid,))
    vdata = mycursor.fetchall()
    
    return render_template('book.html',msg=msg,data=data,act=act,pdata=pdata,vdata=vdata)

@app.route('/user_status', methods=['GET', 'POST'])
def user_status():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
        
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.uname=%s order by b.id desc",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('user_status.html',data=data,act=act,data2=data2)

@app.route('/user_pay', methods=['GET', 'POST'])
def user_pay():
    msg=""
    act=""
    uname=""
    name=""
    name2=""
    mobile=""
    mobile2=""
    mess=""
    mess2=""
    bid=request.args.get("bid")
    vid=request.args.get("vid")
    st=""
    data2=[]
    d2=[]
    if 'username' in session:
        uname = session['username']
        
    now = datetime.datetime.now()
    pdate=now.strftime("%d-%m-%Y")

    t = time.localtime()
    ptime = time.strftime("%H:%M:%S", t)

    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_user where uname=%s",(uname, ))
    data = mycursor.fetchone()
    name=data[1]
    mobile=str(data[4])

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.uname=%s && b.id=%s",(uname,bid))
    data2 = mycursor.fetchone()
    amount=str(data2[18])

    mycursor.execute("SELECT * FROM ar_booking where id=%s",(bid, ))
    d1 = mycursor.fetchone()
    provider=d1[2]

    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(provider, ))
    d2 = mycursor.fetchone()
    name2=d2[1]
    mobile2=str(d2[4])
    

    if request.method=='POST':
        transid=request.form['transid']
        reviews=request.form['reviews']
        
        mycursor.execute("update ar_booking set status=2,transid=%s,pdate=%s,ptime=%s,reviews=%s where id=%s", (transid,pdate,ptime,reviews,bid))
        mydb.commit()
        mycursor.execute("update ar_vehicle set status=0 where id=%s", (vid,))
        mydb.commit()

        mess="Amount Paid: Rs. "+amount
        mess2="Rs."+amount+" Credited from "+uname
        msg="ok"
        
    
    return render_template('user_pay.html',msg=msg,data=data,act=act,data2=data2,d2=d2,mess=mess,mobile=mobile,name=name,mess2=mess2,mobile2=mobile2,name2=name2)

@app.route('/view_pro', methods=['GET', 'POST'])
def view_pro():
    msg=""
    act=""
    uname=request.args.get("uname")
    data2=[]
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ar_vehicle where uname=%s",(uname, ))
    dd2 = mycursor.fetchall()

    for ds2 in dd2:
        dt=[]
        dt.append(ds2[0])
        dt.append(ds2[1])
        dt.append(ds2[2])
        dt.append(ds2[3])
        dt.append(ds2[4])
        dt.append(ds2[5])
        dt.append(ds2[6])
        dt.append(ds2[7])
        dt.append(ds2[8])
        dt.append(ds2[9])
        s1="2"
        ss=""
        mycursor.execute("SELECT count(*) FROM ar_booking where provider=%s && vid=%s && status=0",(uname, ds2[0]))
        cnt3 = mycursor.fetchone()[0]
        if cnt3>0:
            s1="1"
            ss=str(cnt3)

        print("ss="+ss)

        dt.append(ss)
        dt.append(s1)
        data2.append(dt)
        

    return render_template('view_pro.html',msg=msg,data=data,act=act,data2=data2,uname=uname)

@app.route('/pro_history', methods=['GET', 'POST'])
def pro_history():
    msg=""
    act=""
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
        
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ar_provider where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ar_vehicle v,ar_booking b where v.id=b.vid && b.provider=%s && b.status=2 order by b.id desc",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('pro_history.html',data=data,act=act,data2=data2)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
