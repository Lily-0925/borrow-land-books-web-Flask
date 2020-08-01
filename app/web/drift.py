from . import web
from flask_login import login_required,current_user
from flask import flash,redirect,url_for,render_template,request
from app.models.gift import Gift
from app.models.drift import Drift
from app.models.wish import Wish
from app.models.base import db, Base
from app.viewmodel.book import BookViewModel
from app.forms.book import DriftForm
from app.libs.email import send_mail
from sqlalchemy import or_,desc
from app.viewmodel.drift import DriftCollection
from app.libs.enums import PendingStatus
from app.models.user import User
__author__ = '七月'

@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash("This book is in you gift list")
        return redirect(url_for("web.book_detail", isbn=current_user.isbn))
    can_send_drift = current_user.can_send_drift()
    if not can_send_drift:
        return render_template("not_enough_beans.html", beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == "POST" and form.validate():
        save_to_drift(current_gift, form)
        send_mail(current_gift.user.email, "Someone needs request a book from you", "email/get_gift.html",
                  wisher=current_user, gift=current_gift)
    gifter = current_gift.user.summary
    return render_template("drift.html", gifter=gifter, user_beans=current_user.beans, form=form)

@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.requester_id==current_user.id,
                                    Drift.gifter_id==current_user.id)).order_by(desc(Drift.id)).all()
    view = DriftCollection(drifts, current_user.id)
    return render_template("pending.html", drifts=view.data)



@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    try:
        drift = Drift.query.filter(Gift.uid == current_user.id, Drift.id==did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans+=1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    try:
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    try:
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1
        gift = Gift.query.filter_by(id = drift.gift_id,launched = False).first_or_404()
        gift.launched = True
        wish = Wish.query.filter_by(isbn=drift.isbn,uid=drift.requester_id,launched=False).first()
        wish.launched=True
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return redirect(url_for("web.pending"))

def save_to_drift(current_gift,drift_form):
    try:
        drift = Drift()
        drift_form.populate_obj(drift)
        drift.gift_id = current_gift.id
        drift.requester_id=current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)

        drift.book_title=book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        current_user.beans-=1
        db.session.add(drift)
        db.session.commit()
    except Exception as e:
        raise e





