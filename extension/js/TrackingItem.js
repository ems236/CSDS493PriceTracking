// This is a data class that represents a tracked item
class TrackingItem {
    constructor(id, name, amazonUrl, imgUrl, priceThreshold, timeThreshold, sampleFrequency, priceHistory){
        this.id = id;
        this.name = name;
        this.amazonUrl = amazonUrl;
        this.imgUrl = imgUrl;
        this.priceThreshold = priceThreshold;
        this.timeThreshold =  timeThreshold;
        this.sampleFrequency = sampleFrequency;
        this.priceHistory = priceHistory;                  // tuple<date, double>[]
    }
}
