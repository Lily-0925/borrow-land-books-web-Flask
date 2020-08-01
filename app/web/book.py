from flask import jsonify, request, json, render_template,url_for,flash,current_app
from app.libs.helper_function import isbn_or_key
from app.spider.YushuBook import YuShuBook
from . import web
from app.forms.book import searchform
from app.viewmodel.book import BookCollections,BookViewModel
from app.models.gift import Gift
from app.models.wish import Wish
from app.viewmodel.trade import TradeInfo
from flask_login import current_user
@web.route('/book/search')
def search():
    #book/search?q=lily&page=0
    form = searchform(request.args)
    books = BookCollections()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        key_or_isbn = isbn_or_key(q)
        ysb = YuShuBook()
        if key_or_isbn == "isbn":
            ysb.search_for_isbn(q)
        else:
            ysb.search_for_keyword(q, page)
        books.fill(ysb, q)
    else:
        flash("搜索的关键字不符合要求，请重新搜索", category="danger")
    return render_template("search_result.html", books=books)

@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushubook = YuShuBook()
    yushubook.search_for_isbn(isbn)
    book = BookViewModel(yushubook.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gift_info = TradeInfo(trade_gifts)
    trade_wish_info = TradeInfo(trade_wishes)

    return render_template("book_detail.html", book=book, wishes=trade_wish_info, gifts=trade_gift_info,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)

@web.route("/test")
def test():

    return render_template("lily1.html")