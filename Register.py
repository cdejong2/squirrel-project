from flask import Flask, render_template, url_for, flash, redirect, Blueprint
from flask_bcrypt import Bcrypt
from sqlalchemy import exc
from forms import SignupForm

page = Blueprint('page', __name__)

@page.route("/register", methods=['GET', 'POST'])
def register():
    form = SignupForm()
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
            flash(f'Username or email account already exists!', 'failure')
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)
