import decimal

class LoggedPrice:
    def __init__(self, date, price:decimal, primePrice:decimal):
        self.date = date
        self.price = price
        self.primePrice = primePrice

    def __eq__(self, other):
        if isinstance(other, LoggedPrice):
            return (self.primePrice == other.primePrice 
                and self.price == other.price)
        return False
