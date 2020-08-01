from .book import BookViewModel
#from collections import namedtuple

#MyGift = namedtuple("MyGift", ["id", "book", "wishes_count"])

class MyWishes:
    def __init__(self, my_all_wishes, gift_count_dic):
        self.my_all_wishes = my_all_wishes
        self.gift_count_dic = gift_count_dic
        self.wishes = []
        self.parse()

    def parse(self):
        for wish in self.my_all_wishes:
            self.wishes.append({"id":wish.id, "book":BookViewModel(wish.book),
                               "gifts_count":self.gift_count_dic[wish.isbn] if wish.isbn in self.gift_count_dic else 0})



