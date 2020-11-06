import pytest 
from server.shared.related_item_scraper import related_item_scraper

def test_no_related_items():
    assert related_item_scraper('https://www.amazon.com/Manfrotto-MTPIXI-WH-PIXI-Tripod-White/dp/B00G88UND8XM') == []

def test_invalid_item():
    assert related_item_scraper("https://www.amazon.com/Mega-Construx-Probuilder-Grayskull-Multicolor/dp/B07HKV9539/") == []

def test_has_related_items():
    assert related_item_scraper("https://www.amazon.com/gp/product/B01D9OS5KA")[0].id == 0
    assert related_item_scraper("https://www.amazon.com/gp/product/B01D9OS5KA")[0].itemUrl == 'https://www.amazon.com/gp/product/B01F9MQI3G' or 'https://www.amazon.com/gp/product/thematic-highly_rated_B086D4CP3X'
    assert related_item_scraper("https://www.amazon.com/gp/product/B01D9OS5KA")[0].referrerItemId == 'https://www.amazon.com/gp/product/B01D9OS5KA'
    assert related_item_scraper("https://www.amazon.com/gp/product/B01D9OS5KA")[0].name == 'Large Teaspoon Set,16 Pcs 6.7&quot; Silver Spoons,Premium Food Grade 18/10 Stainless Steel Tea Spoons,Durable Metal Teaspoons,Small Silverware Spoons,Kitchen Spoons Set,Mirror Finish &amp; Dishwasher Safe' or 'Stainless Steel Flatware - Silverware Set for 4-20 Piece Cutlery Set - 18/10 Flatware Set - Silverwear Set - Dinnerware Stainless Steel Flatware Set - Spoons and Forks Set Stainless Steel'
    assert related_item_scraper("https://www.amazon.com/gp/product/B01D9OS5KA")[0].imgUrl == 'https://m.media-amazon.com/images/I/31zMte+zM3L._AC_UL480_SR480,480_.jpg' or 'https://m.media-amazon.com/images/I/41tLMcko91L._AC_UL480_SR480,480_.jpg'
    assert related_item_scraper("https://www.amazon.com/gp/product/B01D9OS5KA")[0].price == 11.99 or 22.95