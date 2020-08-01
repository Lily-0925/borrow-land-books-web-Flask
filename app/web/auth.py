from . import web
from flask import render_template, request,redirect,url_for,flash
from app.forms.auth import RegisterForm, LoginForm,EmailForm,ResetPassWordForm
from app.models.user import User
from app.models.base import db, Base
from flask_login import login_user, logout_user

__author__ = '七月'

@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            user = User()
            user.set_sttrs(form.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("web.login"))
        except Exception as e:
            db.session.rollback()
            raise e
    return render_template("auth/register.html", form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True) #cookie
            next = request.args.get("next")
            if not next or not next.startswith("/"):
                next = url_for("web.index")
            return redirect(next)
        else:
            flash("The email dose not exist or the password is wrong")
    return render_template("auth/login.html", form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == "POST":
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first()
            if not user:
                flash("This email is not exist")
            from app.lib.email import send_mail
            send_mail(form.email.data, "reset your password", "email/reset_password.html", user=user,
                      token=user.reset_password())
            flash("We have sent a email to you, please check out")
    return render_template("auth/forget_password_request.html", form=form)



@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPassWordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.password.data)
        if success:
            flash("your password has been reseted, please login again")
            return redirect(url_for("web.login"))
        else:
            flash("Reseting password failed")
    return render_template("auth/forget_password.html",form=form)



@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("web.login"))
    pass
