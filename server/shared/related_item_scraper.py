import urllib.request
import re
from .similar_item import SimilarItem
import pytest 

def related_item_scraper(url):
    related_items = []
    
    # Get html of item page 
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')]
    urllib.request.install_opener(opener)

    # If url is invalid, return an empty list
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return []

    html_contents = response.read()
    html = html_contents.decode("utf-8")
    
    # Store information about each related item into items[]
    section = re.search('SponsoredProductsSimsDpDesktop(.*)', html).group()
    items = re.split('a-carousel-card+', section)    # index 0 is before carousel info
    
    # Only return a max of 10 related items
    num_items = max(10, len(items)-1)
    
    # Get 4 related items
    for i in range(1, num_items):
        # Get item URL
        asin = re.search('sp_detail_(.*?)\" data', items[i]).group(1)
        itemUrl = "https://www.amazon.com/gp/product/" + asin
        
        # Get item name
        name = re.search('title=\"(.*?)\"', items[i]).group(1)
        
        # Get image URL
        img_regex = re.compile('(?=(https://m.media.*?480,480_.jpg))')
        img_matches = img_regex.findall(items[i])
        imgUrl = min(img_matches, key=len)
        
        # Get price
        priceString = re.search(r'\$\d+(?:.(\d+))', items[i]).group()
        price = float(priceString[1:])
        
        # The item's id should not be 0.
        # The item's referrerItemId field should contain id not url
        item = SimilarItem(0, itemUrl, url, name, imgUrl, price)
        related_items += [item]
        
    return related_items   