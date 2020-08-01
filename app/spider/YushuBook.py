from app.libs.Http import HTTP
from flask import current_app

class YuShuBook:
    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"
    def __init__(self):
        self.total = 0
        self.books = []

    def search_for_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_for_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config["PER_PAGE"], self.creat_start(page))
        result = HTTP.get(url)
        self.__fill_collections(result)

    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collections(self,data):
        self.total = data["total"]
        self.books = data["books"]


    def creat_start(self,page):
        return (page-1)*current_app.config["PER_PAGE"]

    @property
    def first(self):
        return self.books[0] if self.total>=1 else None
