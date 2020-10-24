class TrackingItem:
    def __init__(self):
        pass

    @classmethod
    def fromDBRecord(cls, id, url, priceThreshold, timeThreshold, sampleFrequency, priceHistory):
        newItem = TrackingItem()
        newItem.id = id
        newItem.url = url
        newItem.timeThreshold = timeThreshold
        newItem.sampleFrequency = sampleFrequency
        newItem.priceHistory = priceHistory