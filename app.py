from flask import Flask, render_template, request, url_for, request
import firebase_admin
from firebase_admin import db,credentials
import datetime

cred = credentials.Certificate("api/key.json")
firebase_admin.initialize_app(cred,{"databaseURL":'https://coursework-7e5bd-default-rtdb.asia-southeast1.firebasedatabase.app'})
ref = db.reference("/items")

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
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
            itemUpload = ref.child(request.form['item_name'])
            itemUpload.set({
                'description': request.form['item_desc'],
                'date': datetime.datetime.now().strftime("%D"),
                'location': request.form['item_location'],
                'owner': request.form['item_owner'],
                'isFound': False,
            })
            return 'Form submitted! Thank you for reporting!'
        else:
            return 'Missing values: {}'.format(form_errors)
    else:
        return render_template('index.html')

@app.route('/view', methods=['POST','GET'])
def view():
    if request.method =='POST':
        data = ref.get()  # Retrieve data from Firebase

        return render_template('view.html', data=data)
    else:
        return render_template('view.html')
    
@app.route('/markFound', methods=['POST','GET'])
def markFound():
    if request.method=='POST':
        print('hello!')
        item_name = request.form['item_name']
        if item_name =="":
            return 'Missing values: Name'
        else:
            itemEdit = ref.child(item_name)
            itemEdit.update({'isFound': True})
            return 'Item edit successful! please check the database!'

    else:
        return render_template('markFound.html')
if __name__ == "__main__":
    app.run(debug=True)

#TO DO:
#3. Edit database data
#4. Styling
#4. Login authorisation OPTIONAL
