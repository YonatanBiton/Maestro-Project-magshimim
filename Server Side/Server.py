import os
from flask import Flask, request, redirect, render_template, session
from Models.Learn import learn_from_dataset, generate_output
from Models.Linker import Linker

UPLOAD_FOLDER = 'Server Side\Dataset\\'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET'])
def get_index():
    return render_template('client.html', MidiLinkPaste='http://127.0.0.1:5000/Dataset/2021-01-25_175809_02.mid')


@app.route('/signup', methods=['GET'])
def get_register():
    return render_template('singup.html')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/Dataset/<file_name>', methods=['GET'])
def get_midi_files(file_name):
    midi_file = open(f'Dataset/{file_name}', 'rb')
    midi_file_content = midi_file.read()
    midi_file.close()
    return midi_file_content


@app.route('/', methods=['POST'])
def post_index():
    for midi_file in request.files.getlist('midFile'):
        if midi_file.filename.endswith('.mid'):
            filename = midi_file.filename
            midi_file.save(f'{UPLOAD_FOLDER}{filename}')
    return redirect(request.url)


@app.route('/learn', methods=['POST'])
def post_learn():
    learn_from_dataset(UPLOAD_FOLDER, 5)
    generate_output(UPLOAD_FOLDER, 1)
    return redirect('/')