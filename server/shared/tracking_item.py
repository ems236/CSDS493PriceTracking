import datetime 
import dateutil.parser
import decimal

class TrackingItem:
    def __init__(self, id, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency, priceHistory):
        self.id = id
        self.url = url
        self.imgUrl = imgUrl
        self.title = title
        self.timeThreshold = timeThreshold
        self.priceThreshold = priceThreshold
        self.sampleFrequency = sampleFrequency
        self.priceHistory = priceHistory

    SAMPLE_HOUR = 1
    SAMPLE_DAY = 2
    SAMPLE_WEEK = 3

    @classmethod
    def fromDBRecord(cls, id, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency):
        return TrackingItem(id, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency, [])

    @classmethod
    def fromDict(cls, objdict, validator):
        if objdict is None:
            return None

        params = ["id", "url", "imgUrl", "title", "priceThreshold", "timeThreshold", "sampleFrequency"]
        
        attrs = []

        for param in params:
            if param in objdict:
                attrs.append(objdict[param])
            else:
                attrs.append(None)
        
        #add empty price log
        attrs.append([])
        newObj = TrackingItem(*attrs)

        if validator(newObj):
            return newObj
        else:
            return None

    def isValidInsert(self):
        props = [
            (self.url, str),
            (self.imgUrl, str),
            (self.priceThreshold, str),
            (self.timeThreshold, str),
            (self.title, str),
            (self.sampleFrequency, int),
        ]

        for item in props:
            if item[0] is None or not isinstance(item[0], item[1]):
                return False
        
        #everything else might as well let db validate
        return self.isValidTrackingData()

    def isValidUpdate(self):
        props = [
            (self.id, int),
            (self.priceThreshold, str),
            (self.timeThreshold, str),
            (self.sampleFrequency, int),
        ]

        for item in props:
            if item[0] is None or not isinstance(item[0], item[1]):
                return False
        

        #everything else might as well let db validate
        return self.id > 0 and self.isValidTrackingData()

    def isValidTrackingData(self):
        isValidPrice = False
        try:
            self.timeThreshold = dateutil.parser.parse(self.timeThreshold)
            self.priceThreshold = decimal.Decimal(self.priceThreshold)
            isValidPrice = self.priceThreshold >= 0.0

        except Exception:
            return False

        isValidSample = TrackingItem.SAMPLE_HOUR <= self.sampleFrequency and self.sampleFrequency <= TrackingItem.SAMPLE_WEEK
        return isValidSample and isValidPrice

    def __eq__(self, other):
        if isinstance(other, TrackingItem):
            return (self.id == other.id 
                and self.url == other.url 
                and self.imgUrl == other.imgUrl
                and self.title == other.title
                and self.timeThreshold == other.timeThreshold
                and self.sampleFrequency == other.sampleFrequency
                and self.priceHistory == other.priceHistory)
        return False

    def toDict(self):
        itemDict = {
            "id": self.id,
            "priceThreshold": str(self.priceThreshold),
            "timeThreshold": self.timeThreshold.isoformat(),
            "url": self.url,
            "imgUrl": self.imgUrl,
            "title":self.title,
            "sampleFrequency":self.sampleFrequency,
            "priceHistory":[]
        }
        for price in self.priceHistory:
            priceDict = {
                "date": price.date.isoformat(),
                "price": str(price.price),
                "primePrice": str(price.primePrice)
            }
            itemDict["priceHistory"].append(priceDict)

        return itemDict