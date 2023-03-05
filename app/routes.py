from flask import Flask, request, flash, url_for, redirect, render_template, json
from app import app
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db=client.ProjectManager
login_data=db.login


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('uname') 
        password = request.form.get('password')
        # data = userLogin.query.get(user_name)
        x=login_data.find_one({"uname":user_name})
        if  x!=None:
            pwd=x['password']
            print(user_name,pwd)
        else:
            print("Error")
        if password == pwd:
            if user_name == 'Admin':
                return redirect(url_for('view_progress'))
            else:
                return redirect(url_for('add_details',user_name=user_name))
    return render_template('login.html')

@app.route('/home',methods=['GET'])
def home():
    return render_template('dashboard.html')

@app.route('/addtasks',methods=['GET','POST'])
def addtasks():
    db=client.ProjectManager
    taskdb=db.taskdatabase
    tasks=taskdb.find()
    # for t in tasks:
    #     taskdata.append(t[''])
    if request.method=='POST':
        if request.form.get('create')=='create':
            print("Save button clicked")
            notation=request.form.get('newcell1')
            print(notation)
            duration=request.form.get('newcell2')
            taskname=request.form.get('newcell3')
            pred=request.form.get('newcell4')
            taskdb.update_one({"notation":notation},{"$set":{"duration":duration,"task_name":taskname,"predecessor_notn":pred}},upsert=True)
            # return render_template('create_proj.html',tasks=tasks)
            return redirect(url_for('addtasks'))
        elif request.form.get('addRow')=='addRow':
            print("Add row clicked")
            return render_template('create_proj.html',tasks=tasks)
    return render_template('create_proj.html',tasks=tasks)
# @app.route('/admin', methods=['GET', 'POST'])
# def view_progress():
#     if request.method == 'POST':
#         return redirect(url_for('add_mem'))
#     data=userLogin.query.all()
#     return render_template('2nd.html',data=data)

@app.route('/addmember',methods=['GET','POST'])
def add_mem():
    db=client.ProjectManager
    login=db.login
    db=client.ProjectManager
    users=db.members

    if request.method=='POST':
        user_name= request.form.get('Username')
        password = request.form.get('password')
        login.update_one({"uname":user_name},{"$set":{"password":password}},upsert=True)
        users.insert_one({"username":user_name})
        # flash('Record was successfully added')
        return render_template('add_member.html')
    return render_template('add_member.html')

def addtasks(user_name,task_desc):
    memtasks=db.mem_tasks
    new_dict={'task_not':task_desc,'status':0}
    memtasks.update_one({"uname":user_name},{"$push":{'tasklist':new_dict}},upsert=True)
    print("Added tasks")

@app.route('/viewdetails/<user_name>',methods=['GET','POST'])
def view_details(user_name):
    db=client.ProjectManager
    users=db.members
    user =users.find_one({"username":user_name})
    # task = tasks.query.filter_by(username=user_name).all()
    Tasks=db.taskdatabase
    
    memtasks=db.mem_tasks
    task=memtasks.find_one({"uname":user_name})
    list_task=[]
    if task != None:
        for t in task['tasklist']:
            print(t)
            f=Tasks.find_one({"notation":t['task_not']})
            new_dict={"task_name":f['task_name'],"status":t['status']}
            list_task.append(new_dict)
    if request.method=='POST':
        print("POST")
        if request.form.get("add")=='add':
            addtasks(user_name,request.form['task_desc'])
        # task = tasks.query.filter_by(username=user_name).all()
        return redirect(url_for('view_details',user_name=user_name))
    return render_template('mem_details.html',user=user,task=list_task)
    # return redirect(url_for('view_details',user_name=user_name))

@app.route('/adddetails/<user_name>',methods=['GET','POST'])
def add_details(user_name):
    # task = tasks.query.filter_by(username=user_name).all()
    db=client.ProjectManager
    users=db.members
    User=users.find_one({"username":user_name})
    if request.method=='POST':
        users.update_one({"username":user_name},{"$set":{"name":request.form['name'],"address":request.form['address'],"phone_no":request.form['phno'],"role":request.form['part']}},upsert=True)
        selitems = request.form.getlist("sel_items")
        print("selected")
        print(selitems)
        for s in selitems:
            pass
            # d = tasks.query.filter_by(id=s).first()
            # d.status=1
    return render_template('team_mem.html',user=User)
    
    # User = userDetails.query.filter_by(username=user_name).first()
    # if User is not None:
    #     return render_template('team_mem.html', user=User,task=task)
        
    # User = userDetails(
    #     user_name, " "," "," "," ")
    # try:
    #         db.session.add(User)
    #         db.session.commit()
    #         print('Added successfully')
    #         return render_template('team_mem.html', user=User)
    # except:
    #         return "Error adding to database"
