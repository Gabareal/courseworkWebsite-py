from flask import Flask, render_template, request, url_for, request, session,redirect
import firebase_admin
from firebase_admin import db,credentials, auth,storage
import datetime
import uuid
from uuid import uuid4

cred = credentials.Certificate("api/key.json")
firebase_admin.initialize_app(cred,{"databaseURL":'https://coursework-7e5bd-default-rtdb.asia-southeast1.firebasedatabase.app'})
bucket = storage.bucket("coursework-7e5bd.appspot.com")
ref = db.reference("/items")

app = Flask(__name__)

    
@app.route('/', methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/protected')
def protected():
    return render_template('protected.html')

@app.route('/addUsers')
def addUsers():
    return render_template('addUsers.html')

@app.route('/generateKey')
def generateKey():
    return render_template('databaseKey.html')

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
         # Get image file from form
        image_file = request.files['image']

        # Save the image file to a local temporary directory
        image_path = "../img"
        image_file.save(image_path)

        # Create new token
        img_src = "items/" + request.form['item_name'] + ".png"
        blob = bucket.blob(img_src)
        metadata = {"firebaseStorageDownloadTokens": request.form['item_name']} # Set metadata for the image
        blob.metadata = metadata # Upload the image file to Firebase Storage
        blob.upload_from_filename(filename=image_path, content_type='image/png')
        blob.make_public() # Make the image publicly accessible
        image_url = blob.public_url # Get the public URL of the uploaded image
        image_metadata = {
            'filename': img_src,
            'url': image_url,
            'timestamp': str(datetime.datetime.now())
        } # Store metadata about the uploaded image in Firebase Realtime Database
        if len(form_errors) == 0:
            itemUpload = ref.child(request.form['item_name'])
            itemUpload.set({
                'description': request.form['item_desc'],
                'date': datetime.datetime.now().strftime("%D"),
                'location': request.form['item_location'],
                'owner': request.form['item_owner'],
                'isFound': False,
                'imgurl': image_metadata['url']
            })
            return 'Form submitted! Thank you for reporting!'
        else:
            return 'Missing values: {}'.format(form_errors)
    else:
        return render_template('report.html')

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
