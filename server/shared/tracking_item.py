class TrackingItem:
    def __init__(self, id, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency, priceHistory):
        self.id = id
        self.url = url
        self.imgUrl = imgUrl
        self.title = title
        self.timeThreshold = timeThreshold
        self.sampleFrequency = sampleFrequency
        self.priceHistory = priceHistory

    @classmethod
    def fromDBRecord(cls, id, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency, priceHistory):
        return TrackingItem(id, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency, priceHistory)

    @classmethod
    def fromFrontEnd(cls, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency):
        return TrackingItem(-1, url, imgUrl, title, priceThreshold, timeThreshold, sampleFrequency, [])

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