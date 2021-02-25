import os
from flask import Flask, request, redirect
from Models.Learn import learn_from_dataset, generate_output

UPLOAD_FOLDER = 'Server Side\Dataset\\'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def get_index():
    html_file = open(f'{os.getcwd()}\Client Side\client.html', 'r')
    html_file_content = html_file.read().replace('@MidiLinkPaste', f'http://127.0.0.1:5000/Dataset/2021-01-25_175809_02.mid')
    html_file.close()
    return html_file_content

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

@app.route('/Dataset/<file_name>', methods=['GET'])
def get_midi_files(file_name):
    midi_file = open(f'{os.getcwd()}\Server Side\Dataset\{file_name}', 'rb')
    midi_file_content = midi_file.read()
    midi_file.close()
    return midi_file_content