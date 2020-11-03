class SimilarItem:
    def __init__(self, itemUrl, referrerItemId, name, imgUrl, price):
        self.itemUrl = itemUrl
        self.referrerItemId = referrerItemId
        self.name = name
        self.imgUrl = imgUrl
        self.price = price

    @classmethod
    def fromDict(cls, objdict):
        if objdict is None:
            return None
            
        params = [
            ("itemUrl", str), 
            ("imgUrl", str),
            ("name", str),
            ("referrerItemId", int),
            ("price", float),
        ]
        
        attrs = []

        for param in params:
            if param[0] in objdict and isinstance(param[0], param[1]):
                attrs += objdict[param]
            else:
                return None
        
        #add empty price log
        attrs += []
        newObj = SimilarItem(*attrs)

        #let sql deal with the strings
        if newObj.referrerItemId >= 1 and newObj.price >= 0:
            return newObj
        else:
            return None


    def __eq__(self, other):
        if isinstance(other, SimilarItem):
            return (self.itemUrl == other.itemUrl 
                and self.imgUrl == other.imgUrl 
                and self.name == other.name
                and self.referrerItemId == other.referrerItemId
                and self.price == other.price)
        return False