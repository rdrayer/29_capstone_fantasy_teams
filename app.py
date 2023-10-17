from flask import Flask, jsonify, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickens"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fantasyteams'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        session['username'] = new_user.username

        db.session.add(new_user)
        db.session.commit()

        flash('Welcome! Account successfully created', 'success')
        return redirect('/fantasy.html')
    return render_template('/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome {user.username}!", "success")
            session['username'] = user.username
            return redirect('/fantasy')
        else: 
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)

@app.route('/fantasy')
def fantasy():
    return render_template('/fantasy.html')