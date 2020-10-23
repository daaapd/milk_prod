from flask import Flask,render_template,request
#,redirect,url_for
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
UPLOAD_FOLDER = '/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
#def index():
#    return redirect(url_for('hello'))

#@app.route('/hello/')
#@app.route('/hello/<name>')
#def hello(name = None):
#    return render_template('hello.html',name=name)




@app.route('/upload/',methods = ['GET','POST'])
def upload():
    if request.method =='POST':
        file = request.files['file']
        print('test')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return render_template('upload.html')
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug = True)