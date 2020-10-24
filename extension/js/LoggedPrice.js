// This data class represents a logged price for an item
class LoggedPrice{
    constructor(logDate, price, primePrice) {
        this.logDate = logDate;
        this.price = price;
        this.primePrice = primePrice;
    }

    priceFor(isPrime) {
        if (isPrime == true) {
            return this.primePrice
        } else {
            return this.price
        }
    } 

}