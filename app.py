from flask import Flask, render_template, request, url_for, request
import firebase_admin
from firebase_admin import db,credentials

cred = credentials.Certificate("api/key.json")
firebase_admin.initialize_app(cred,{"databaseURL":'https://coursework-7e5bd-default-rtdb.asia-southeast1.firebasedatabase.app'})
ref = db.reference("/")


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
    
def index():
    if request.method == 'POST':
        form_errors = ""
        if request.form['item_name'] == "":
            form_errors += "Name "
        if request.form['item_desc'] == "":
            form_errors += "Description "
        if request.form['item_date'] == "":
            form_errors += "Date "
        if request.form['item_location'] == "":
            form_errors += "Location "
        if request.form['item_owner'] == "":
            form_errors += "Owner "
        if len(form_errors) == 0:
            itemUpload = ref.child(request.form['item_name'])
            itemUpload.set({
                'description': request.form['item_desc'],
                'date': request.form['item_date'],
                'location': request.form['item_location'],
                'owner': request.form['item_owner'],
                'isFound': False,
            })
            return 'Form submitted :3'
        else:
            return 'Missing values: {}'.format(form_errors)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)