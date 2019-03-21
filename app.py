from flask import Flask, render_template
from data import Articles
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host/database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://noor:Nurzhamal@165.227.110.208/noor'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
health = HealthCheck(app, "/healthy")
envdump = EnvironmentDump(app, "/environment")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


app = Flask(__name__)

Articles = Articles()
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
