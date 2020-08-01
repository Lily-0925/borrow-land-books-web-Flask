from . import web
from app.models.base import db
from flask_login import login_required,current_user
from app.models.wish import Wish
from flask import flash, url_for,redirect,render_template
from app.viewmodel.wish import MyWishes
from app.models.gift import Gift
from app.libs.email import send_mail
__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    my_all_wishes = Wish.get_user_wish(uid)
    isbn_list = [wish.isbn for wish in my_all_wishes]
    gift_count_dic = Wish.get_gift_count(isbn_list)
    #{"23424563366":1, "32453464342":2}
    view_model = MyWishes(my_all_wishes, gift_count_dic)
    return render_template("my_wish.html", wishes=view_model.wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        try:
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        flash("This book has benn added to your gift list or wish list,please try another one")
    return redirect(url_for("web.book_detail", isbn=isbn))

@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    wish = Wish.query.filter_by(id=wid, launched=False).first_or_404()
    gift = Gift.query.filter_by(id=current_user.id, launched=False, isbn=wish.isbn).first()
    if not gift:
        flash("This book is not in your gift list,please firstly add it in your book list")
    else:
        send_mail(wish.user.email,"someone wants to send you a book","email/satisify_wish.html",wish=wish,gift=gift)
        flash("a email has been sent to that person")
    return render_template(url_for("web.book_detail", isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    wish.status = 0
    db.session.commit()
    return redirect(url_for("web.my_wish"))
