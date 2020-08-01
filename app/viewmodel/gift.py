from .book import BookViewModel
from collections import namedtuple

#MyGift = namedtuple("MyGift", ["id", "book", "wishes_count"])

class MyGifts:
    def __init__(self, my_all_gifts, wish_count_dic):
        self.my_all_gifts = my_all_gifts
        self.wish_count_dic = wish_count_dic
        self.gifts = []
        self.parse()

    def parse(self):
        for gift in self.my_all_gifts:
            self.gifts.append({"id":gift.id, "book":BookViewModel(gift.book),
                               "wishes_count":self.wish_count_dic[gift.isbn]
                               if gift.isbn in self.wish_count_dic else 0})



