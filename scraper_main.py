from server.shared.price_scraper import price_scraper
from server.shared.tracking_item_dal import TrackingItemDAL
from server.shared.tracking_item import TrackingItem

from datetime import datetime
from decimal import Decimal

class ScraperTask():
    def __init__(self):
        self.dal = TrackingItemDAL()
    
    def scrape_all_prices(self):
        toScrape = self.dal.itemsToScrape()
        for item in toScrape:
            self.scrape_price(item[0], item[1])

    def scrape_price(self, itemid: int, itemUrl: str):
        try:
            price = price_scraper(itemUrl)
            self.dal.logPrice(itemid, Decimal(price), Decimal(price))
        except: 
            pass
        


if __name__ == "__main__":
    scraper = ScraperTask()
    scraper.scrape_all_prices()
