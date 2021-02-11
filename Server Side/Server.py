from flask import Flask

UPLOAD_FOLDER = 'Dataset'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def get_index():
    return "../Clien Side/client.html"

@app.route('/', methods=['POST'])
def post_index():
    if 'midFile' not in request.files:
        return redirect(request.url)
    midi_file = request.files['midFile']
    if midi_file.filename.endswith('.mid'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(request.url)