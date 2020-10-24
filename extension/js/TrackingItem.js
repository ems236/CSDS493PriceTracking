// This is a data class that represents a tracked item
class TrackingItem {
    constructor(id, amazonUrl, priceThreshold, timeThreshold, sampleFrequency, priceHistory){
        this.id = id;
        this.amazonUrl = amazonUrl;
        this.priceThreshold = priceThreshold;
        this.timeThreshold =  timeThreshold;
        this.sampleFrequency = sampleFrequency;
        this.priceHistory = priceHistory;                  // tuple<date, double>[]
    }
}