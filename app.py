from flask import Flask, jsonify, request, render_template, redirect, flash, session, g
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Team, Player
from forms import RegisterForm, LoginForm, TeamForm, PlayerForm

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

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if 'username' in session:
        g.user = User.query.filter(User.username == session['username']).first()

    else:
        g.user = None

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
        return redirect('/teams')
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
            return redirect('/teams')
        else: 
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)

@app.route('/teams')
def display_teams():
    teams = Team.query.all()
    return render_template('/teams.html', teams=teams)

@app.route('/logout')
def logout():
    session.pop('username') 
    return redirect('/')

@app.route('/teams/new', methods=['GET', 'POST'])
def create_team():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = TeamForm()
    user = g.user
    if form.validate_on_submit():
        name = form.name.data
        sport = form.name.data

        new_team = Team(name=name, sport=sport, user_id=user.user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect('/teams')
    return render_template('/create_team.html', form=form)

@app.route('/teams/<int:team_id>/add', methods=['GET', 'POST'])
def add_players(team_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    team = Team.query.get(team_id)

    form = PlayerForm()
    if form.validate_on_submit():
        name = form.name.data
        position = form.position.data

        split_name = name.split(' ')
        api_url = 'https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={0}%20{1}'.format(split_name[0], split_name[1])
        response = requests.get(api_url)
        data = response.json()
        if data == {'player': None}:
            flash("Please enter a valid athlete.", "danger")
        elif data != {'player': None}:
            new_player = Player(name=name, position=position, user_id=g.user.user_id, team_id=team.team_id)
            db.session.add(new_player)
            db.session.commit()
            return redirect(f'/teams/{team.team_id}/detail')

    return render_template('/add_players.html', form=form)

@app.route('/teams/<int:team_id>/detail', methods=['GET', 'POST'])
def display_players(team_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    team = Team.query.get(team_id)
    players = Player.query.filter(Player.team_id == team.team_id)
    print('PRINTINGINSOIJFLSJF')
    print(players)
    return render_template('team_detail.html', team=team, players=players)
