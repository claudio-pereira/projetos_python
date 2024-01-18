import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf.csrf import CSRFProtect
from forms import LoginForm

load_dotenv()

# Criação de instâncias Flask e extensões
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

csrf = CSRFProtect(app)
# Configuração do banco de dados SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Rota para raiz
@app.route('/')
def index():
    return render_template('index.html')

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

# Rota para dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Welcome, {current_user.username}!'

# Rota para logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))