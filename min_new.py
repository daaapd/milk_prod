# -*- coding: utf8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import analis
UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#print(basedir)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def template(data):
    return render_template('hello.html', items=data)

@app.route('/')
@app.route('/index')
def index():
   return render_template("hello.html")
def hello(name = None):
    return render_template('hello.html')
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        for f in request.files.getlist('file'):
          if f and allowed_file(file.filename):
            #print(f.filename)
            filename = f.filename.replace(' ','_')#secure_filename(f.filename)
            print(filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
        return template(files)#render_template('hello.html')
    return '''
    <!doctype html>
    <meta charset="UTF-8">
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file multiple="">
         <input type=submit value=Upload>
    </form>
    '''
#@app.context_processor
@app.route('/report')
def report():
    print('test')
    analis.analis_image()
    return render_template('hello.html')

@app.route('/test')
def test():
    analis.analis_image()
    return "nothing"

from flask import send_from_directory

@app.route('/uploaded_file.csv')
def uploaded_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                              'wub.csv')

if __name__=="__main__":
     app.run(port=5555,debug=True)