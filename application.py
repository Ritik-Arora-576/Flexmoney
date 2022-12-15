from flask import Flask, render_template, request, redirect, session
import os
import pickle as pkl
from datetime import date
from dateutil.relativedelta import relativedelta

application = Flask(__name__)
application.secret_key = os.urandom(24)

@application.route('/')
def home():
    return render_template("register.html",status='4')

@application.route('/register', methods=['POST'])
def register():
    with open('database/users.pkl', 'rb') as f:
        dict = pkl.load(f)
    name=request.form['name']
    p_no=request.form['number']
    age=int(request.form['age'])
    batch=request.form['batch']
    due_date=date.today()
    key=name+str(p_no)
    id=len(dict)+1
    if key in dict:
        return render_template("register.html",status='1')
    if age<18 or age>65:
        return render_template("register.html",status='2')
    dict[key] = {'id':id, 'name':name, 'p_no':p_no, 'age':age, 'batch': batch,'due_date':due_date}
    with open('database/users.pkl', 'wb') as f:
        pkl.dump(dict, f)
    return render_template("register.html",status='3')

@application.route('/login')
def login():
    if 'member' in session:
        return redirect('/detail')
    return render_template('login.html',status='0')

@application.route('/check', methods=['POST'])
def check():
    if 'member' in session:
        return redirect('/detail')
    with open('database/users.pkl', 'rb') as f:
        dict = pkl.load(f)
    name=request.form['name']
    p_no=request.form['number']
    key=name+str(p_no)
    if key in dict:
        session['member']=dict[key]
        return render_template('details.html', detail=dict[key])
    return render_template('login.html',status='1')

@application.route('/detail')
def detail():
    if 'member' not in session:
        return redirect('/login')
    return render_template('details.html', detail=session['member'])

@application.route('/admin')
def admin():
    if 'admin' in session:
        return redirect('/update')
    return render_template('admin.html',status='0')

@application.route('/check-admin',methods=['POST'])
def checkAdmin():
    with open('database/admin.pkl', 'rb') as f:
        dict = pkl.load(f)
    
    if dict['id']==request.form['emp_id'] and dict['password']==request.form['password']:
        session['admin']=dict['password']
        return redirect('/update')

    return render_template('admin.html',status='1')

@application.route('/update')
def update():
    if 'admin' not in session:
        return redirect('/admin')
    return render_template("update.html",status='4')

@application.route('/check-update', methods=['POST'])
def checkUpdate():
    if 'admin' not in session:
        return redirect('/admin')
    with open('database/users.pkl', 'rb') as f:
        dict = pkl.load(f)
    name=request.form['name']
    p_no=request.form['number']
    paid=request.form['paid']
    batch=request.form['batch']
    key=name+str(p_no)

    if key not in dict:
        return render_template("update.html",status='1')

    d1=date.today()
    d2=dict[key]['due_date']
    remain=(d1-d2).days

    if paid!='yes' and remain<=0:
        return render_template("update.html",status='2')

    dict[key]['due_date']=d1+ relativedelta(months=+1)

    if batch!="none":
        dict[key]['batch']=batch
    with open('database/users.pkl', 'wb') as f:
        pkl.dump(dict, f)
    return render_template("update.html",status='3')

@application.route('/backToLogin',methods=['POST'])
def backToLogin():
    session.pop('member')
    return redirect('/login')

@application.route('/backToAdmin',methods=['POST'])
def backToAdmin():
    session.pop('admin')
    return redirect('/admin')

application.run(debug=True)