import urllib.request

# url = "https://www.amazon.com/gp/product/B01D9OS5KA?pf_rd_r=08EESWMRZMTND4DA059Y&pf_rd_p=edaba0ee-c2fe-4124-9f5d-b31d6b1bfbee"
# url = "https://www.amazon.com/gp/product/B081SH4YGV/ref=ewc_pr_img_1?smid=ATVPDKIKX0DER&psc=1
# url = "https://www.amazon.com/Elite-Gourmet-Maxi-Matic-EBM8103B-Programmable/dp/B08BSP4GL1?smid=ATVPDKIKX0DER&pf_rd_r=JXY27TP1NNM8WG7DX86A&pf_rd_p=4dce43a3-83a3-42ca-a1d5-26d9f5bc7b11"

def price_scraper(url):    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')]
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url)
    html_contents = response.read()
    html = html_contents.decode("utf-8")
    
    buybox_start_index = html.find("price_inside_buybox")
    buybox_end_index = html.find("price_inside_buybox_badge")
    buybox_html = html[buybox_start_index:buybox_end_index]

    price_start_index = buybox_html.find("$")+1
    price_end_index = buybox_html.find("\n</span>")
    price_string = buybox_html[price_start_index:price_end_index]
    price = float(price_string)
    return price