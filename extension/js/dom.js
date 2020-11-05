/*
  dom.js: act as a placeholder to parse a product's information
          and return the information to the extension's popup window.

  Expected to be removed
*/

// Add an event listener
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
				
	var imgSrc = document.getElementById('landingImage').src;
	var productName = document.getElementById('productTitle').innerHTML;
	
	// Parse all similar items
	var similarItems = document.getElementsByClassName("a-carousel-card aok-float-left");
	var similarItemImgSrc = [];
	var similarItemName = [];
	var similarItemPrice = [];
	var similarItemUrl = [];
	for (var i = 0; i < similarItems.length; i++) {
       similarItemImgSrc[i] = similarItems[i].getElementsByTagName('img')[0].getAttribute("src");
	   similarItemName[i] = similarItems[i].getElementsByTagName('div')[2].innerHTML.trim();
	   similarItemPrice[i] = similarItems[i].getElementsByClassName("p13n-sc-price")[0].innerHTML.trim();
	   similarItemUrl[i] = "https://www.amazon.com" +similarItems[i].getElementsByTagName('a')[0].getAttribute("href");
	   //console.log(similarItemImgSrc[i]);
	   //console.log(similarItemName[i]);
	   //console.log(similarItemPrice[i]);
	   //console.log(similarItemUrl[i]);
    }
	
    
	
	// Handle products without default buybox
	// "Buy new" "buy used"
	var productPrice = "$0.00";
	var newProductExists = document.getElementById('newBuyBoxPrice');
	
	if (newProductExists) {
		productPrice = document.getElementById('newBuyBoxPrice').innerHTML;
	} else {
		productPrice = document.getElementById('price_inside_buybox').innerHTML;
	}
	
	// Handle products unavailable to be shipped
	var shipping = "";
	var normalProduct = document.getElementById('exports_desktop_qualifiedBuybox_tlc_feature_div').getElementsByClassName('a-size-base a-color-secondary');
	if (normalProduct.length != 0) {
		shipping = normalProduct[0].innerHTML;
	} else {
		var unavailableExists = document.getElementById('deliveryMessageMirId').getElementsByClassName('a-color-error');
	    if (unavailableExists.length != 0) {
		   shipping = unavailableExists[0].innerHTML;
	    } 
	}
	
	
	if (request.greeting == "hello")
      sendResponse({imgSrc: imgSrc, 
                    name: productName, 
                    price: productPrice, 
                    shipping: shipping, 
                    similarImgSrc: similarItemImgSrc,
                    similarItemName: similarItemName,
                    similarItemPrice: similarItemPrice,
					similarItemUrl: similarItemUrl
					});
  });
