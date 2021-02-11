import os
from flask import Flask, request, redirect
from Models.Learn import learn_from_dataset, generate_output

UPLOAD_FOLDER = 'Server Side\Dataset\\'
DATASET_PATH = '"Server Side"\Dataset'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def get_index():
    html_file = open(f'{os.getcwd()}\Client Side\client.html', 'r')
    return html_file.read()


@app.route('/', methods=['POST'])
def post_index():
    for midi_file in request.files.getlist('midFile'):
        if midi_file.filename.endswith('.mid'):
            filename = midi_file.filename
            midi_file.save(f'{UPLOAD_FOLDER}{filename}')
    return redirect(request.url)


@app.route('/learn', methods=['POST'])
def post_learn():
    learn_from_dataset(DATASET_PATH, 5)
    generate_output(DATASET_PATH, 1)
    return redirect('/')
