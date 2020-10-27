class SimilarItem:
    def __init__(self, itemUrl, referrerItemId, name, imgUrl, price):
        self.itemUrl = itemUrl
        self.referrerItemId = referrerItemId
        self.name = name
        self.imgUrl = imgUrl
        self.price = price

    def __eq__(self, other):
        if isinstance(other, SimilarItem):
            return (self.itemUrl == other.itemUrl 
                and self.imgUrl == other.imgUrl 
                and self.name == other.name
                and self.referrerItemId == other.referrerItemId
                and self.price == other.price)
        return False