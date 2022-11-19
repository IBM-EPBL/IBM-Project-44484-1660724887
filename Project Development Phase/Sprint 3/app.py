import fileinput
import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.python.keras.models import load_model
from keras.api._v2.keras.preprocessing import image
#from tensorflow.keras.preprocessing import image

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app=Flask(__name__)
print("check")
model_filename = (os.path.join(os.getcwd(),'model','fruitsmodel.h5'))
print(model_filename)
model = load_model(model_filename)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('Image Prediction.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:

            ('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('starting img procesing')
            result = imageProcessing(file=file)
            flash('Predicted Result : '+result)
            return redirect('/')
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)

def imageProcessing(file):
    filenamevar = file.filename
    filepath = os.path.join(os.getcwd(),'uploads',filenamevar)
    print(filepath)
    img = image.load_img(filepath,target_size=(64,64))
    x = image.img_to_array(img)
    x=np.expand_dims(x, axis=0)
    pred = np.argmax(model.predict(x), axis=1)
    index = ['DATES-carbs:75g,Iron:6%,protein:2.5g','GUAVA-Fat:1g,Carbohydrate:14g,Sugar:9g','ORANGE-Fat:0.1g,Potassium:181mg,Sugar:9g','PINEAPPLE-Fat:0.1g,Carbohydrate:13g,Sugar:10g','WATERMELON-Fat:0.2g,Carbohydrate:8g,Sugar:6g']
    text=str(index[pred[0]])
    print(text)
    return text

@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/Diet')
def DietChart():
    return render_template("Diet Chart.html")


@app.route('/Importance')
def ImportanceofFood():
    return render_template("Importance of Food.html")

@app.route('/task')
def task():
    return render_template("task.html")


if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = 5000, debug=False)
