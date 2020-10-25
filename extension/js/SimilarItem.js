// This is a data class that represents a similar item
class SimilarItem {
    constructor(amazonUrl, referrerItem, name, imgUrl, price){
        this.amazonUrl = amazonUrl;
        this.referrerItem = referrerItem;
        this.name = name;
        this.imgUrl = imgUrl;
        this.price = price;
    }
}
module.exports = SimilarItem