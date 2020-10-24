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
	var productPrice = document.getElementById('price_inside_buybox').innerHTML;
	var shipping = document.getElementById('shippingMessageInsideBuyBox_feature_div').getElementsByClassName('a-size-base a-color-secondary')[0].innerHTML;
    
	if (request.greeting == "hello")
      sendResponse({imgSrc: imgSrc, name: productName, price: productPrice, shipping: shipping});
  });