class TradeInfo:
    def __init__(self, goods):
        self.total = len(goods) if goods else 0
        self.trades = [self.one_to_map(single) for single in goods] if goods else []

    def one_to_map(self, single):
        dic = {"user_name":single.user.nickname, "id":single.id}
        return dic