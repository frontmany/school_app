from flask import Blueprint, render_template, redirect, flash, url_for, request
import os
from ..functions import save_picture
from ..forms import RegistrationForm, LoginForm
from ..extensions import db
from ..models.user import User
from flask_login import login_user, logout_user



user = Blueprint('user', __name__)



@user.route('/user/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        avatar_filename = save_picture(form.avatar.data)
        user = User(name=form.name.data, login=form.login.data, avatar=avatar_filename, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Поздравляем, {form.login.data}! Вы успешно зарегистрированы", "success")
            return redirect(url_for('user.login'))
        
        except Exception as e:
            print(e)
            flash(f"При регистрации произошла ошибка", "danger")
        

    return render_template('user/register.html', form=form)



@user.route('/user/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and (user.password == form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Поздравляем, {form.login.data}! Вы успешно авторизованы", "success")
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash(f"Ошибка входа", "danger")

    return render_template('user/login.html', form=form)

@user.route('/user/logout', methods=['POSt', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('post.all'))