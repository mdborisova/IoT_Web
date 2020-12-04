from random import randint

from .models import Data, User
from . import create_app, db

from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

app = create_app()


# API
@app.route('/api/getAllData', methods=['GET'])
@login_required
def get_data():
    data = Data.query.all()[0]
    data_json = {
        "BATTERY": randint(0, 100),
        "TEMP_1": randint(-20, 50) if data.on else 0,
        "TEMP_2": randint(-20, 50) if data.on else 0,
        "TEMP_3": randint(-20, 50) if data.on else 0,
        "IS_ON": data.on
    }
    return jsonify(data_json)


@app.route('/api/changeState/isOn', methods=['POST'])
@login_required
def change_state_on_off():
    data = Data.query.all()[0]
    data.on = int(request.form['newState'])
    db.session.commit()
    return jsonify({"result": 1})


# LOGIN
@app.route('/login')
def login():
    data = dict(title='Login')
    return render_template('login.html', **data)


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not user.password == password:  # check_password_hash(user.password, password)
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# MAIN
@app.errorhandler(404)
@login_required
def page_not_found(e):
    data = dict(title='Page Not Found', name=current_user.name)
    return render_template('404.html', **data)


@app.route('/')
@login_required
def index():
    data = dict(title='Dashboard', name=current_user.name)
    return render_template('index.html', **data)


@app.route('/profile')
@login_required
def profile():
    data = dict(title='Profile', email=current_user.email, name=current_user.name)
    return render_template('profile.html', **data)


if __name__ == '__main__':
    app.run()
