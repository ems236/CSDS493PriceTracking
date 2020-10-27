import urllib.request
import re
from similar_item import SimilarItem

# url = "https://www.amazon.com/gp/product/B01D9OS5KA?pf_rd_r=08EESWMRZMTND4DA059Y&pf_rd_p=edaba0ee-c2fe-4124-9f5d-b31d6b1bfbee"
# url = "https://www.amazon.com/gp/product/B081SH4YGV/ref=ewc_pr_img_1?smid=ATVPDKIKX0DER&psc=1
# url = "https://www.amazon.com/Elite-Gourmet-Maxi-Matic-EBM8103B-Programmable/dp/B08BSP4GL1?smid=ATVPDKIKX0DER&pf_rd_r=JXY27TP1NNM8WG7DX86A&pf_rd_p=4dce43a3-83a3-42ca-a1d5-26d9f5bc7b11"

def related_item_scraper(url):
    related_items = []
    
    # Get html of item page 
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')]
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url)
    html_contents = response.read()
    html = html_contents.decode("utf-8")
    
    # Store information about each related item into items[]
    section = re.search('SponsoredProductsSimsDpDesktop(.*)SponsoredProductsViewability', html).group()
    items = re.split('a-carousel-card+', section)    # index 0 is before carousel info
    
    # Get 4 related items
    for i in range(1, 5):
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
        
        # The item's referrerItemId field stores the url instead of id. Change later.
        item = SimilarItem(itemUrl, url, name, imgUrl, price)
        related_items += [item]
        
    return related_items   