from server.shared.price_scraper import price_scraper
import pytest

# pytest --cov=. 

def test_no_price():
    assert price_scraper("https://www.amazon.com/Mounted-Handmade-Entryway-Bathroom-Organizer/dp/B07L99BTQK") == "NoPriceError"

def test_invalid_item():
    assert price_scraper("https://www.amazon.com/Hodedah-4-Shelve-Bookcase-Cherry/dp/B05XY6WZLP") == "InvalidItemError"

def test_valid_price():
    assert price_scraper("https://www.amazon.com/Uniden-BCD436HP-HomePatrol-TrunkTracker-Programming/dp/B00I33XDAK") == 490.22
