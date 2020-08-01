from . import web
from app.viewmodel.book import BookViewModel
from app.models.gift import Gift
from flask import render_template


__author__ = '七月'


@web.route('/')
def index():
    recent_gift = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gift]
    return render_template("index.html", recent=books)


@web.route('/personal')
def personal_center():
    pass
