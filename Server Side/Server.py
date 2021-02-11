import os
from flask import Flask, request, redirect
from Models.Learn import learn_from_dataset, generate_output

UPLOAD_FOLDER = 'Server Side\Dataset\\'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def get_index():
    html_file = open(f'{os.getcwd()}\Client Side\client.html', 'r')
    return html_file.read()

@app.route('/', methods=['POST'])
def post_index():
    if 'midFile' not in request.files:
        return redirect(request.url)
    midi_file = request.files['midFile']
    print(midi_file)
    if midi_file.filename.endswith('.mid'):
        filename = midi_file.filename
        midi_file.save(f'{UPLOAD_FOLDER}{filename}')
    return redirect(request.url)

@app.route('/learn', methods=['POST'])
def post_learn():
    learn_from_dataset(UPLOAD_FOLDER, 5)
    generate_output(UPLOAD_FOLDER, 1)
    return redirect('/')