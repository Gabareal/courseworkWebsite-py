from flask import Flask, render_template, request, url_for, request
import datetime
import pyrebase
config = {
  "apiKey": "AIzaSyBBKv0bFftovEPZhZ_k2XbjrEoATf68O1A",
  "authDomain": "coursework-7e5bd.firebaseapp.com",
  "databaseURL": "https://coursework-7e5bd-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "coursework-7e5bd",
  "storageBucket": "coursework-7e5bd.appspot.com",
  "messagingSenderId": "627904949119",
  "appId": "1:627904949119:web:ff6f3d641483b3690ac84a",
  "measurementId": "G-7B1CH7BFJR",
  "serviceAccount": "serviceAccount.json",
  "databaseURL" : "https://coursework-7e5bd-default-rtdb.asia-southeast1.firebasedatabase.app"
 }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
#storage = firebase.storage()



app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(user_email, user_password)
            return "Login successful!"
        except ValueError as e:
            return "Authentication failed: {}".format(e)
    else:
        return render_template('login.html')

@app.route('/report', methods=['POST','GET'])
def report():
    if request.method == 'POST':
        form_errors = ""
        if request.form['item_name'] == "":
            form_errors += "Name "
        if request.form['item_desc'] == "":
            form_errors += "Description "
        if request.form['item_location'] == "":
            form_errors += "Location "
        if request.form['item_owner'] == "":
            form_errors += "Owner "
        if len(form_errors) == 0:
            data = {
                'description': request.form['item_desc'],
                'date': datetime.datetime.now().strftime("%D"),
                'location': request.form['item_location'],
                'owner': request.form['item_owner'],
                'isFound': False,
            }
            db.child("items").child(request.form['item_name']).set(data)
            return 'Form submitted! Thank you for reporting!'
        else:
            return 'Missing values: {}'.format(form_errors)
    else:
        return render_template('report.html')

@app.route('/view', methods=['POST','GET'])
def view():
    if request.method =='POST':
        data = db.child("items").get().val()
        formatted_data = [{"name": key, **value} for key, value in data.items()]
        return render_template('view.html', data=formatted_data)

    else:
        return render_template('view.html')
    
@app.route('/markFound', methods=['POST','GET'])
def markFound():
    if request.method=='POST':
        item_name = request.form['item_name']
        if item_name =="":
            return 'Missing values: Name'
        else:
            db.child("items").child(item_name).update({'isFound': True})
            return 'Item edit successful! please check the database!'
    else:
        return render_template('markFound.html')
if __name__ == "__main__":
    app.run(debug=True)
