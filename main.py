from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif'}

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def processImage(filename,operation):
    img = cv2.imread(f"uploads/{filename}")
    if operation == "cgray":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newFilename = f"static/{filename}"
        cv2.imwrite(newFilename,imgProcessed)
        return newFilename
    elif operation == 'cwebp':
        newFilename = f"static/{filename.split('.')[0]}.webp"
        cv2.imwrite(newFilename,img)
        return newFilename
    elif operation == 'cpng':
        newFilename = f"static/{filename.split('.')[0]}.png"
        cv2.imwrite(newFilename,img)
        return newFilename
    elif operation == 'cjpg':
        newFilename = f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(newFilename,img)
        return newFilename

@app.route("/")
def home():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/edit",methods = ["GET","POST"])
def edit():
    if request.method == 'POST':
        operation = request.form.get('operation')
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "Error : No file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ni = processImage(filename,operation)
            flash(f"Your image has been processed and is available <a href= '/{ni}' target='_blank'> here </a>")
            return render_template('index.html')
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/how")
def how():
    return render_template("how.html")

app.run(debug=True)