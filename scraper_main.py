from server.shared.price_scraper import price_scraper
from server.shared.tracking_item_dal import TrackingItemDAL
from server.shared.tracking_item import TrackingItem

from datetime import datetime
from decimal import Decimal

class ScraperTask():
    def __init__(self):
        self.dal = TrackingItemDAL(True)
    
    def scrape_all_prices(self):
        toScrape = self.dal.itemsToScrape()
        for item in toScrape:
            self.scrape_price(item)

    def scrape_price(self, item : TrackingItem):
        try:
            price = price_scraper(item.url)
            self.dal.logPrice(item.id, Decimal(price), Decimal(price))
        except: 
            pass
        


if __name__ == "__main__":
    scraper = ScraperTask()
    scraper.scrape_all_prices()
