from flask import Flask, render_template, url_for, flash, \
    redirect, request, abort
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user
from sqlalchemy import exc
from forms import LoginForm, RegistrationForm, SearchForm
import pandas as pd
from squirrelapi import find_squirrel, stringme

# Boilerplate code from previous project --- To Be Replaced
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '25d5ad000a6a0c19ef1dc9c409582f31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return f"User('{self.email}')"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',
                           subtitle='Home Page',
                           text='Welcome to Squirrel Collector!')


@app.route("/login", methods=['GET', 'POST'])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.

    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = (bcrypt.generate_password_hash(form.password.data)
                    .decode('utf-8'))
        user = User(email=form.email.data,
                    password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash(f'Username or email account already exists!', 'success')
        else:
            flash(f'Account created for {form.email.data}!', 'success')
            return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/learn")
def learn():
    return render_template(
        'learn.html',
        subtitle='Learn',
        text='More information about the Squirrel Census and the \
        API will be provided here.')


@app.route("/listen")
def listen():
    TITLE = "Listen"
    FILE_NAME = "Squirrel Chirping and Barking.wav"
    return render_template('listen.html', songName=TITLE, file=FILE_NAME)


@app.route("/squirrel_search", methods=['GET', 'POST'])
@login_required
def squirrel_search():
    form = SearchForm()
    if form.validate_on_submit():
        number = form.hectare_number.data
        letter = form.hectare_letter.data
        hectare = number + letter
        print(hectare)
        flash(f'Searching in hectare {hectare}', 'success')
        return redirect(url_for('squirrels_found', hectare=hectare))
    return render_template('squirrel_search.html', form=form)
                        
                        
@app.route("/squirrels_found", methods=['GET', 'POST'])
@login_required
def squirrels_found():
    hectare = request.args.get('hectare', None)
    squirrels = find_squirrel(hectare)
    squirrel_list = []
    for idx, row in squirrels.iterrows():
        print(stringme(row))
        squirrel_list.append(row)
    if request.method == 'POST':
        print(request.form.getlist('squirrel'))
        
    return render_template('squirrels_found.html', data=squirrel_list, stringme=stringme)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
