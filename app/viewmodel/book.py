class BookViewModel:
    def __init__(self, book):
        self.title = book["title"]
        self.publisher = book["publisher"]
        self.pages = book["pages"] or ""
        self.author = "、".join(book["author"])
        self.price = book["price"]
        self.summary = book["summary"] or ""
        self.isbn = book["isbn"]
        self.image = book["image"]
        self.pubdate = book["pubdate"]
        self.binding = book["binding"]
    @property  
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return "/".join(intros)

class BookCollections:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''
    def fill(self,YuShuBook,keyword):
        self.total = YuShuBook.total
        self.books = [BookViewModel(book) for book in YuShuBook.books]
        self.keyword = keyword

