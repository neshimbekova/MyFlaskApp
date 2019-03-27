from flask import Flask, render_template, flash, redirect, url_for, session, request
from data import Articles
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
#from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host/database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://noor:Nurzhamal@165.227.110.208/noor'
app.config['SECRET_KEY'] = 'secret_littlesnowflake<<>>kuku'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


# Register Form Class
# class RegisterForm(FlaskForm):
#     name = StringField('Name', [validators.Length(min=1, max=50)])
#     username = StringField('Username', [validators.Length(min=4, max=25)])
#     email = StringField('Email', [validators.Length(min=6, max=50)])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords do not match')])
#     confirm = PasswordField('Confirm Password')
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

#HealthCheck
@app.route('/healthy', methods=['GET'])
def healthy():
    return jsonify({'message': 'ok'})

#HomePage
Articles = Articles()
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

#AboutPage
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

#SignUP_Page
@app.route("/signup", methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1> New User Has been created! </h1>'
    return render_template('signup.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

#Logout_Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('home.html')



@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
