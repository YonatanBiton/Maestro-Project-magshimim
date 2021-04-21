from flask import Flask, request, redirect, render_template, session
from Core.Learn import learning_thread 
from Models.Linker import Linker
from Models.User import User
from Models.MaestroException import MaestroException
import Core.Check
import threading
import os
import random
import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET'])
def get_index():
    try:
        logged_user = User(session)
        return render_template('client.html', MidiLinkPaste=f'http://127.0.0.1:5000/Dataset/{logged_user.name}')
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
            folder_path = f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{folder_name}'
            try:
                file_name = random.choice(os.listdir(folder_path))
            except IndexError:
                return ""
            midi_file = open(os.path.join(folder_path, file_name), 'rb')
            midi_file_content = midi_file.read()
            midi_file.close()
        return midi_file_content
    except Exception:
        return ""

@app.route('/login', methods=['POST'])
def post_login():
    required_args = [
        'username',
        'password'
    ]
    errors = []
    if not Core.Check.are_args_in_form(request.form, required_args, errors):
        return render_template('login.html', ErrorMessage=" ".join(errors))
    logged_user = Linker().login_user(request.form['username'], request.form['password'])
    if logged_user != None:
        if logged_user.active != 1:
            return redirect('/login')
        session['logged_user'] = logged_user.to_json()
        logged_user.create_folder_if_no_exists(Config.UPLOAD_FOLDER)
    return redirect('/') if logged_user != None else redirect('/login')


@app.route('/signup', methods=['POST'])
def post_signup():
    Core.Check.check_signup_request()
    registered_user = Linker().register_user(request.form['username'], request.form['password'], request.form['email'])
    if registered_user != None:
        session['logged_user'] = registered_user.to_json()
        registered_user.create_folder_if_no_exists(Config.UPLOAD_FOLDER)
    return redirect('/') if registered_user != None else redirect('/signup')


@app.route('/', methods=['POST'])
def post_index():
    if 'logged_user' in session:
        required_args = [
            'name',
            'active',
            'password',
            'email'
        ]
        if not Core.Check.are_args_in_form(session['logged_user'], required_args):
            return redirect(request.url)
        logged_user = User(session['logged_user'])
        if logged_user.active != 1:
            return redirect(request.url)
        logged_user.create_folder_if_no_exists(Config.UPLOAD_FOLDER)
        for midi_file in request.files.getlist('midFile'):
            if midi_file.filename.endswith('.mid'):
                filename = midi_file.filename
                midi_file.save(f'{os.getcwd()}/Server Side/{Config.UPLOAD_FOLDER}{logged_user.name}/{filename}')
    return redirect(request.url)


@app.route('/learn', methods=['POST'])
def post_learn():
    if 'logged_user' not in session:
        return redirect('/')
    required_args = [
        'name',
        'active',
        'password',
        'email'
    ]
    if not Core.Check.are_args_in_form(session['logged_user'], required_args):
        return redirect('/')
    logged_user = User(session['logged_user'])
    if logged_user.active != 1:
        return redirect('/')
    logged_user.create_folder_if_no_exists(Config.UPLOAD_FOLDER)
    learn_thread = threading.Thread(target=learning_thread, args=(f'"Server Side"/{Config.UPLOAD_FOLDER}{logged_user.name}', 5, 1)) 
    learn_thread.start()
    return redirect('/')