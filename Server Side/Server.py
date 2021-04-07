from flask import Flask, request, redirect, render_template, session
from Models.Learn import learning_thread 
from Models.Linker import Linker
from Models.User import User
import Models.Check
import threading
import os
import random

UPLOAD_FOLDER = 'Dataset/'

app = Flask(__name__)
app.secret_key = '842jkfhsjdfhHJKFAH89421)(@#*jdjsahf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET'])
def get_index():
    if 'logged_user' not in session:
        return redirect('/login')
    required_args = [
        'name',
        'active',
        'password',
        'email'
    ]
    if not Models.Check.are_args_in_form(session['logged_user'], required_args):
        return redirect('/login')
    logged_user = User(session['logged_user'])
    logged_user.create_folder_if_no_exists(UPLOAD_FOLDER)
    return render_template('client.html', MidiLinkPaste=f'http://127.0.0.1:5000/Dataset/{logged_user.name}')


@app.route('/signup', methods=['GET'])
def get_register():
    return render_template('singup.html')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/home', methods=['GET'])
def get_home():
    return render_template('home.html') 


@app.route('/Dataset/<folder_name>', methods=['GET'])
def get_midi_files(folder_name):
    required_args = [
        'name',
        'active',
        'password',
        'email'
    ]
    midi_file_content = ""
    if 'logged_user' in session:
        if not Models.Check.are_args_in_form(session['logged_user'], required_args):
            return ""
        logged_user = User(session['logged_user'])
        if logged_user.name == folder_name and logged_user.active == 1:
            logged_user.create_folder_if_no_exists(UPLOAD_FOLDER)
            folder_path = f'{os.getcwd()}/Server Side/{UPLOAD_FOLDER}{folder_name}'
            try:
                file_name = random.choice(os.listdir(folder_path))
            except IndexError:
                return ""
            midi_file = open(os.path.join(folder_path, file_name), 'rb')
            midi_file_content = midi_file.read()
            midi_file.close()
    return midi_file_content


@app.route('/login', methods=['POST'])
def post_login():
    required_args = [
        'username',
        'password'
    ]
    errors = []
    if not Models.Check.are_args_in_form(request.form, required_args, errors):
        return render_template('login.html', ErrorMessage=" ".join(errors))
    logged_user = Linker().login_user(request.form['username'], request.form['password'])
    if logged_user != None:
        if logged_user.active != 1:
            return redirect('/login')
        session['logged_user'] = logged_user.to_json()
        logged_user.create_folder_if_no_exists(UPLOAD_FOLDER)
    return redirect('/') if logged_user != None else redirect('/login')


@app.route('/signup', methods=['POST'])
def post_signup():
    required_args = [
        'username',
        'password',
        'email'
    ]
    errors = []
    if not Models.Check.are_args_in_form(request.form, required_args, errors) or not Models.Check.is_password_confirmed(request.form, errors): 
        return render_template('singup.html', ErrorMessage=" ".join(errors))
    registered_user = Linker().register_user(request.form['username'], request.form['password'], request.form['email'])
    if registered_user != None:
        session['logged_user'] = registered_user.to_json()
        registered_user.create_folder_if_no_exists(UPLOAD_FOLDER)
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
        if not Models.Check.are_args_in_form(session['logged_user'], required_args):
            return redirect(request.url)
        logged_user = User(session['logged_user'])
        if logged_user.active != 1:
            return redirect(request.url)
        logged_user.create_folder_if_no_exists(UPLOAD_FOLDER)
        for midi_file in request.files.getlist('midFile'):
            if midi_file.filename.endswith('.mid'):
                filename = midi_file.filename
                midi_file.save(f'{os.getcwd()}/Server Side/{UPLOAD_FOLDER}{logged_user.name}/{filename}')
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
    if not Models.Check.are_args_in_form(session['logged_user'], required_args):
        return redirect('/')
    logged_user = User(session['logged_user'])
    if logged_user.active != 1:
        return redirect('/')
    logged_user.create_folder_if_no_exists(UPLOAD_FOLDER)
    learn_thread = threading.Thread(target=learning_thread, args=(f'{UPLOAD_FOLDER}{logged_user.name}', 5, 1)) 
    learn_thread.start()
    return redirect('/')