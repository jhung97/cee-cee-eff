from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, jsonify
import os
import socket
import subprocess
from werkzeug.utils import secure_filename
from handle_file import handle_file, handle_field, handle_form, ALLOWED_EXTENSIONS
from FieldUtils.process_scan import process
from FieldUtils.upload_ICR import icrify
import random
import json

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    #DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    #USERNAME='admin',
    #PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

CUR_DIR = os.getcwd()

UPLOAD_FOLDER = CUR_DIR + '/handler/uploaded_files'
OUTPUT_FOLDER = CUR_DIR + '/handler/output_files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['INTER_FOLDER'] = CUR_DIR + '/handler/inter_imgs'

def allowed_file(filename):
    return '.' in filename and \
           '.' + filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect('/ncr')

@app.route('/ncr')
def ncr():
    #Clear filse before we start
    clear_folders = ['handler/uploaded_files', 'handler/inter_imgs']
    for folder in clear_folders:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)

            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    return render_template('file_input.html')

def return_failed(message):
    diction = {'result':'failed', message:message}
    return json.dumps(diction)

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print str(message)

    return dict(mdebug=print_in_console)


@app.route("/upload_file", methods=['POST'])
def upload_file():
    clear_folders = ['handler/uploaded_files', 'handler/inter_imgs']
    for folder in clear_folders:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)

            try:
                if os.path.isfile(file_path) and file.startswith(("SIN","Existing","phone","excel",'stone',"bridgehouse")):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.close()
            return "Image Uploaded"
    return redirect(request.url)

@app.route("/process_file", methods=['GET', 'POST'])
def process_file():
    #print("testing")
    if request.method == 'POST':

        data = request.data
        form  = request.form
        files = request.files
        # print(data)
        # print(form)
        # print(files)


        # print(data[2])

        is_field = request.form['is_field']
        #print(is_field)

        # if 'file' not in request.form:
        #     return redirect(request.url)

        if not is_field:
            #print("debug")
            flash("Must specify if image is a field or individual file")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #print("debug 2")
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.close()
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            rnd = str(random.randint(0, 25))

            #Pass to form detector iff it's a form. 
            if is_field == 'field':
                #print("in a field")
                output = handle_field(path)
                return jsonify({ 'is_field': is_field, 'filename':filename, 'filepath':path, 'output': output })
            elif is_field == 'form':
                output = process(path)
                print(filename)
                return jsonify({ 'is_field': is_field, 'filename':filename, 'filepath':path, 'output': output })

    return
    # return render_template('file_input.html')

@app.route('/uploaded_files/<path:filename>')
def uploaded_files(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)

@app.route('/inter_files/<path:filename>')
def inter_files(filename):
    return send_from_directory(directory=app.config['INTER_FOLDER'], filename=filename)

@app.route("/crash", methods=['GET'])
def crashing():
    raise ValueError("error raised")
    return

if __name__ == '__main__':
app.run(port=5000)