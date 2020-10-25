class LoggedPrice:
    def __init__(self, date, price, primePrice):
        self.date = date
        self.price = price
        self.primePrice = primePrice

    def __eq__(self, other):
        if isinstance(other, LoggedPrice):
            return (self.date == other.date 
                and self.primePrice == other.primePrice 
                and self.price == other.price)
        return False
