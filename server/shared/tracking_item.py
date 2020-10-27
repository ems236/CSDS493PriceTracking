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