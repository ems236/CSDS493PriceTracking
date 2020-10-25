/*
  popup.js: act as a placeholder to get a product's information
            by sending a request to the eventlistner definied in dom.js
			and display the information on extension's popup window.

  TODO: should be handling information from the backend
*/
console.log('popup.js.');

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
    
	// Get response from current product page
	console.log("imgSrc: " + response.imgSrc);
	console.log("product name: " + response.name.trim());
	console.log("product price: " + response.price);
	console.log("product shipping fee: " + response.shipping.trim());
	console.log(tabs[0].url);
	
	// Set clickable image and direct detail page to the product 
	document.getElementById('card-link-title-1').setAttribute("href", tabs[0].url);
	document.getElementById('card-link-footer-1').setAttribute("href", tabs[0].url);
	
	// Set first product information
	document.getElementById('img-card1').setAttribute("src", response.imgSrc);
		
	// Handle possible shipping fee
	var price = response.price.trim();
	var shippingFee = response.shipping.trim();
	
	// Handle products that cannot be shipped
	if (shippingFee.includes("$")){
	   shippingFee = shippingFee.substring(shippingFee.indexOf("$") + 1, shippingFee.indexOf("Shipping") - 1);
	} else {
	   shippingFee = "0.00";
	}
	var totalAmt = parseFloat(price.substring(1, price.length)) + parseFloat(shippingFee);
	//console.log("total amount: " + totalAmt);
	//document.getElementById('current-price-card1').setAttribute(innerHTML, totalAmt.toPrecision(4));
	$("#current-price-card1").text("$" + totalAmt.toPrecision(4));
	
	// Trim product name when it's too long
	var productName = response.name.trim();
	var productNameShortened = productName;
	if (productName.includes(",")){
		productNameShortened = productName.substr(0, productName.indexOf(","));
	} 
	document.getElementById('card-title1').innerHTML = productNameShortened;
    
  });
});

//
