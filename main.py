from flask import Flask, render_template, url_for, flash, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from sqlalchemy import exc
from forms import SignupForm
from Register import page

# Blanket code from previous project --- To Be Replaced
app = Flask(__name__)
app.register_blueprint(page)
proxied = FlaskBehindProxy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '25d5ad000a6a0c19ef1dc9c409582f31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@app.route("/")
def home():
    return render_template('home.html',
                           subtitle='Home Page',
                           text='This is the home page')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")