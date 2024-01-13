from flask import Flask,render_template,request,url_for,redirect,session
from pymongo import MongoClient
from bson.objectid import ObjectId

app=Flask(__name__)
app.secret_key="maha"

mongo_hello="mongodb://localhost:27017"
mongo_url=MongoClient(mongo_hello)
db=mongo_url.hospital
collection=db.appoinment

def isloggedin():
    return "username" in session



@app.route('/')
def read():
    data=collection.find({})
    return render_template("index.html",datas=data)


@app.route('/insert',methods=["GET","POST"])
def insert():
    if request.method=="POST":
        name=request.form.get("name")
        age=request.form.get("age")
        gender=request.form.get("gender")
        Appointment_Time=request.form.get("Appointment Time")
        Mobile=request.form.get("Mobile")
        Appointment_Date=request.form.get("Appointment_Date")
        datum={"Name":name,"Age":age,"Gender":gender,"Appointment_time":Appointment_Time,
            "Phone_Number":Mobile,"Appointment_Date":Appointment_Date}
        collection.insert_one(datum)
    data=collection.find({})
    return render_template("index.html",datas=data)


@app.route('/edit/<string:id>',methods=["POST","GET"])
def edit(id):
    order=collection.find_one({"_id":ObjectId(id)})
    if request.method=="POST":
        name=request.form.get("Name")
        age=request.form.get("Age")
        gender=request.form.get("Gender")
        Appointment_Time=request.form.get("Appointment_time")
        Mobile=request.form.get("Phone_Number")
        Appointment_Date=request.form.get("Appointment_Date")
        collection.update_one({"_id":ObjectId(id)},{"$set":{"Name":name,"Age":age,"Gender":gender,
                "Appointment_time":Appointment_Time,"Phone_Number":Mobile,"Appointment_Date":Appointment_Date}})
        return redirect(url_for("read"))
    return render_template("edit.html",order=order)  

@app.route('/delete/<string:id>',methods=["POST","GET"])
def delete(id):
    collection.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('read'))


@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        first_name=request.form.get("first_name")
        last_name=request.form.get("last_name")
        password=request.form.get("password")
        log=db.log.insert_one({"first_name":first_name,"last_name":last_name,"password":password})
        if log:
            session['username']=first_name
            return redirect(url_for('read'))
        else:
            return 'Invalid Credentials'
    return render_template('login.html')


@app.route('/signin',methods=["POST","GET"])
def signin():
    if request.method=="POST":
        signup={
        "first_name":request.form.get("first_name"),
        "last_name":request.form.get("last_name"),
        "password":request.form.get("password")}
    
        db.signup.insert_one(signup)
        return redirect(url_for('login'))
    return render_template("signup.html")
 



if __name__=="__main__":
    app.run(debug=True)