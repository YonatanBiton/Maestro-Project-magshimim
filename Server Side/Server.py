from flask import Flask, request, redirect, render_template, session
from Core.Learn import learning_thread 
from Models.Linker import Linker
from Models.User import User
from Models.MaestroException import MaestroException
import Core.Check
import threading
import os
import glob
import Config
import ntpath

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET'])
def get_index():
    try:
        logged_user = User(session)
        folder_path = f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{logged_user.name}/learning/polyphony_rnn/generated'
        midis_path = f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{logged_user.name}'
        midi_load = ""
        current_file = 0
        current_song_name = ""
        midis_load_files = glob.glob(f"{midis_path}/*.mid")
        midi_files = glob.glob(f"{folder_path}/*.mid")
        if os.path.isdir(folder_path):
            current_file = session['midi_index'] + 1 if 'midi_index' in session and len(midi_files) > 0 else 0
            current_song_name = ntpath.basename(midi_files[session['midi_index']]) if 'midi_index' in session and session['midi_index'] < len(midi_files) else ""
        for file in midis_load_files:
                midi_load += f"<li>{ntpath.basename(file)}</li>"
        template = render_template('client.html', MidiLinkPaste=f'http://127.0.0.1:5000/Dataset/{logged_user.name}', CurrentSongName=current_song_name, CurrentFile=current_file, FilesInLab=len(midi_files))
        template = template.replace('@MidisLoad', midi_load)
        return template
    except Exception:
        return redirect('/login')


@app.route('/signup', methods=['GET'])
def get_register():
    try:
        return render_template('singup.html')
    except Exception:
        return redirect('/home')


@app.route('/login', methods=['GET'])
def get_login():
    try:
        return render_template('login.html')
    except Exception:
        return redirect('/home')


@app.route('/home', methods=['GET'])
def get_home():
    try:
        return render_template('home.html') 
    except Exception:
        return redirect('/')


@app.route('/Dataset/<folder_name>', methods=['GET'])
def get_midi_files(folder_name):
    try:
        midi_file_content = ""
        logged_user = User(session)
        if logged_user.name == folder_name:
            folder_path = f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{folder_name}/learning/polyphony_rnn/generated'
            if not os.path.isdir(folder_path):
                return midi_file_content
            midi_files = glob.glob(f"{folder_path}/*.mid")
            if 'midi_index' not in session or session['midi_index'] >= len(midi_files):
                return midi_file_content
            file_name = ntpath.basename(midi_files[session['midi_index']])
            midi_file = open(os.path.join(folder_path, file_name), 'rb')
            midi_file_content = midi_file.read()
            midi_file.close()
        return midi_file_content
    except Exception:
        return ""


@app.route('/login', methods=['POST'])
def post_login():
    try:
        Core.Check.check_login_request(request.form)
        logged_user = Linker().login_user(request.form['username'], request.form['password'])
        if logged_user == None:
            raise MaestroException('The username or password is incorrect.')
        session['logged_user'] = logged_user.to_json()
        session['midi_index'] = 0
        return redirect('/') 
    except MaestroException as e:
        return render_template('login.html', ErrorMessage=e.error_message)
    except Exception:
        return render_template('login.html')


@app.route('/signup', methods=['POST'])
def post_signup():
    try:
        Core.Check.check_signup_request(request.form)
        registered_user = Linker().register_user(request.form['username'], request.form['password'], request.form['email'])
        if registered_user != None:
            session['logged_user'] = registered_user.to_json()
            session['midi_index'] = 0
        return redirect('/') if registered_user != None else redirect('/signup')
    except MaestroException as e:
        return render_template('singup.html', ErrorMessage=e.error_message)
    except Exception:
        return render_template('singup.html')

@app.route('/', methods=['POST'])
def post_index():
    try:
        logged_user = User(session)
        for midi_file in request.files.getlist('midFile'):
            if midi_file.filename.endswith('.mid'):
                filename = midi_file.filename
                midi_file.save(f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{logged_user.name}/{filename}')
        return redirect(request.url)
    except Exception:
        return redirect(request.url)


@app.route('/learn', methods=['POST'])
def post_learn():
    try:
        logged_user = User(session)
        learn_thread = threading.Thread(target=learning_thread, args=(f'"Server Side"/{Config.UPLOAD_FOLDER}{logged_user.name}', 5, 1)) 
        learn_thread.start()
        return redirect('/')
    except Exception:
        return redirect('/')


@app.route('/next', methods=['POST'])
def post_next():
    try:
        logged_user = User(session)
        folder_path = f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{logged_user.name}/learning/polyphony_rnn/generated'
        if os.path.isdir(folder_path):
            midi_files = glob.glob(f"{folder_path}/*.mid")
            if 'midi_index' in session and len(midi_files) > 0:
                session['midi_index'] = session['midi_index'] + 1 if session['midi_index'] < len(midi_files) - 1 else 0
            else:
                session['midi_index'] = 0
        else:
            session['midi_index'] = 0
        return redirect('/')
    except Exception:
        return redirect('/')


@app.route('/prev', methods=['POST'])
def post_prev():
    try:
        logged_user = User(session)
        folder_path = f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{logged_user.name}/learning/polyphony_rnn/generated'
        if os.path.isdir(folder_path):
            midi_files = glob.glob(f"{folder_path}/*.mid")
            if 'midi_index' in session and len(midi_files) > 0:
                session['midi_index'] = session['midi_index'] - 1 if session['midi_index'] > 0 else len(midi_files) - 1
            else:
                session['midi_index'] = 0
        else:
            session['midi_index'] = 0
        return redirect('/')
    except Exception:
        return redirect('/')