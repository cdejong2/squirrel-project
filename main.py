from flask import Flask, render_template, url_for, flash, \
    redirect, request, abort
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user
from sqlalchemy import exc, text
from map import createMap
from forms import LoginForm, RegistrationForm, SearchForm
import pandas as pd
from squirrelapi import find_squirrel, stringme, strshort
import json

# Boilerplate code from previous project --- To Be Replaced
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '25d5ad000a6a0c19ef1dc9c409582f31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
createMap()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def create_table():
    query = text("""CREATE TABLE IF NOT EXISTS ' {} ' (
    x FLOAT, y FLOAT,
    id STRING NOT NULL PRIMARY KEY,
    hectare STRING,
    shift STRING, date STRING,
    hectare_squirrel_number INT,
    age STRING, primary_fur_color STRING,
    highlight_fur_color STRING,
    combination_primary_and STRING,
    location STRING,
    above_ground_sighter STRING,
    running BOOL, chasing BOOL,
    climbing BOOL, eating BOOL,
    foraging BOOL, other_activities STRING,
    kuks BOOL, quaas BOOL, moans BOOL,
    tail_flags BOOL, tail_twitches BOOL,
    approaches BOOL, indifferent BOOL,
    runs_from BOOL, geocoded_column JSON,
    other_interactions STRING)""".format(str(current_user.get_id())))
    db.engine.execute(query)


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
    flash(f'Logged out!', 'success')
    return redirect(url_for("home"))


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
        subtitle='Learn More About the Squirrels',
        link1='2018 Central Park Squirrel Census',
        link2='The Squirrel Census Project',
        link3='Central Park Squirrels API',
        link4='The Eastern Gray Squirrel')


@app.route("/listen")
def listen():
    FILE_NAME1 = "Squirrel Chirping and Barking.wav"
    FILE_NAME2 = "Squirrel making quaa and kuk sounds.wav"
    FILE_NAME3 = "Gray Squirrel Meowing Sounds.wav"
    CAPTION1 = "Chirping and barking sounds used to alert other \
    squirrels of danger"
    CAPTION2 = "Kuk: a chirpy vocal communication used for a variety \
    of reasons, sometimes to alert of danger"
    CAPTION3 = "Meow or Quaa: an elongated vocal communication which \
    can indicate the presence of a ground predator such as a dog."

    return render_template('listen.html',
                           audio1="Chirps and Barks", cap1=CAPTION1,
                           file1=FILE_NAME1, audio2="Kuks and Quaas",
                           cap2=CAPTION2, file2=FILE_NAME2,
                           audio3="Squirrel Meows", cap3=CAPTION3,
                           file3=FILE_NAME3)


@app.route("/squirrel_search", methods=['GET', 'POST'])
@login_required
def squirrel_search():
    form = SearchForm()
    if form.validate_on_submit():
        number = form.hectare_number.data
        letter = form.hectare_letter.data
        if number < 10:
            number = '0' + str(number)
        else:
            number = str(number)
        letter = letter.upper()
        hectare = number + letter
        print(hectare)
        flash(f'Searching in hectare {hectare}', 'success')
        return redirect(url_for('squirrels_found', hectare=hectare))
    return render_template('squirrel_search.html',
                           subtitle='Look for squirrels:', form=form)


@app.route("/squirrels_found", methods=['GET', 'POST'])
@login_required
def squirrels_found():
    hectare = request.args.get('hectare', None)
    squirrels = find_squirrel(hectare)
    squirrel_list = []
    for idx, row in squirrels.iterrows():
        squirrel_list.append(row)

    if request.method == 'POST':
        index = request.form.getlist('squirrel')
        selected = squirrels.iloc[index]
        selected["geocoded_column"] = selected["geocoded_column"].apply(
            lambda x: json.dumps(x))
        create_table()
        selected.to_sql(current_user.get_id(),
                        con=db.engine,
                        if_exists='append',
                        index=False)
        flash(f'Squirrels added!', 'success')
        return redirect(url_for('home'))

    return render_template('squirrels_found.html', data=squirrel_list,
                           stringme=stringme)


@app.route("/squirrels")
@login_required
def squirrels_showcase():
    try:
        squirrels = pd.read_sql_table(current_user.get_id(),
                                      con=db.engine)
    except ValueError:
        flash(f'No squirrels found!', 'success')
        return redirect(url_for('home'))
    else:
        squirrel_list = []
        for idx, row in squirrels.iterrows():
            squirrel_list.append(row)

        return render_template('showcase.html',
                               subtitle="View your collection!",
                               data=squirrel_list, stringme=strshort)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
