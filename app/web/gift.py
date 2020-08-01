
from . import web
from app.models.base import db
from flask_login import login_required,current_user
from app.models.gift import Gift
from app.viewmodel.gift import MyGifts
from flask import current_app, flash, url_for, redirect,render_template
from app.models.drift import Drift
from app.libs.enums import PendingStatus
__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    my_all_gifts = Gift.get_user_gift(uid)
    isbn_list = [gift.isbn for gift in my_all_gifts]
    wish_count_dic = Gift.get_wish_count(isbn_list)
    #{"23424563366":1, "32453464342":2}
    view_model = MyGifts(my_all_gifts, wish_count_dic)
    return render_template("my_gifts.html", gifts=view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        try:
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config["BEANS_FOR_ONE_BOOK"]
            db.session.add(gift)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        flash("This book has benn added to your gift list or wish list,please try another one")
    return redirect(url_for("web.book_detail", isbn=isbn))



@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first_or_404()
    if drift:
        flash("This book is in dealing status, you cannot recall it")
    else:
        current_user.beans-=current_app.config("BEANS_FOR_ONE_BOOK")
        gift.status = 0
        db.session.commit()
    return redirect(url_for("web.my_gifts"))



