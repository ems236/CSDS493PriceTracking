from decimal import Decimal

class SimilarItem:
    def __init__(self, id, itemUrl, referrerItemId, name, imgUrl, price):
        self.id = id
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
            ("referrerItemId", int),
            ("name", str),
            ("imgUrl", str),
            ("price", str),
        ]
        
        attrs = []

        for param in params:
            if param[0] in objdict and isinstance(objdict[param[0]], param[1]):
                attrs.append(objdict[param[0]])
            else:
                return None
    
        newObj = SimilarItem(-1, *attrs)

        try:
            newObj.price = Decimal(newObj.price)
        except Exception:
            return None

        #let sql deal with the strings
        if newObj.referrerItemId >= 1 and newObj.price >= 0:
            return newObj
        else:
            return None

    def toDict(self):
        return {
            "id": self.id,
            "itemUrl": self.itemUrl,
            "referrerItemId": self.referrerItemId,
            "name": self.name,
            "imgUrl": self.imgUrl,
            "price": str(self.price)
        }

    def __eq__(self, other):
        if isinstance(other, SimilarItem):
            return (self.itemUrl == other.itemUrl 
                and self.imgUrl == other.imgUrl 
                and self.name == other.name
                and self.referrerItemId == other.referrerItemId
                and self.price == other.price)
        return False