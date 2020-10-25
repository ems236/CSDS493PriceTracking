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
	var normalProduct = document.getElementById('shippingMessageInsideBuyBox_feature_div').getElementsByClassName('a-size-base a-color-secondary');
	if (normalProduct.length != 0) {
	   shipping = normalProduct[0].innerHTML;
	} else {
	   var unavailableExists = document.getElementById('deliveryMessageMirId').getElementsByClassName('a-color-error');
	   if (unavailableExists.length != 0) {
	      shipping = unavailableExists[0].innerHTML;
	   } 
	}
    
	if (request.greeting == "hello")
      sendResponse({imgSrc: imgSrc, name: productName, price: productPrice, shipping: shipping});
  });
