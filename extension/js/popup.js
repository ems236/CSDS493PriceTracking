/*
  popup.js: act as a placeholder to get a product's information
            by sending a request to the eventlistner definied in dom.js
			and display the information on extension's popup window.

  TODO: should be handling information from the backend
*/
console.log('popup.js.');

chrome.tabs.query({
  active: true,
  currentWindow: true
}, function(tabs) {
  chrome.tabs.sendMessage(tabs[0].id, {
    greeting: "hello"
  }, function(response) {

    // Get response from current product page
    //console.log("imgSrc: " + response.imgSrc);
    //console.log("product name: " + response.name.trim());
    //console.log("product price: " + response.price);
    //console.log("product shipping fee: " + response.shipping.trim());
    //console.log("similar img urls: " + response.similarImgSrc);
    //console.log("similar item names: " + response.similarItemName);
    //console.log("similar item prices: " + response.similarItemPrice);
    //console.log("similar item urls: " + response.similarItemUrl);
    //console.log(tabs[0].url);

    // Set clickable image and direct detail page to the product 
    document.getElementById('card-link-title-1').setAttribute("href", tabs[0].url);
    //document.getElementById('card-link-footer-1').setAttribute("href", tabs[0].url);

    // Set first product information
    document.getElementById('img-card1').setAttribute("src", response.imgSrc);
	
	// Get unique similar items
	response.similarImgSrc = [...new Set(response.similarImgSrc)];
	response.similarItemName = [...new Set(response.similarItemName)];
	response.similarItemPrice = [...new Set(response.similarItemPrice)];
	response.similarItemUrl = [...new Set(response.similarItemUrl)];
	
    // Default sort similar items
	var idx = [];
    for (var i = 0; i < response.similarItemPrice.length; i++) {
      idx.push(i);
    }
    var comparator = function(arr) {
      return function(a, b) {
		var priceA = arr[a];
        var priceB = arr[b];
        priceA = parseFloat(priceA.substr(1, priceA.length));
        priceB = parseFloat(priceB.substr(1, priceB.length));
        return priceB > priceA ? 1 : -1;
      };
    };
    idx = idx.sort(comparator(response.similarItemPrice));
	
    // Display 10 similar items of a certain product
    function addSimilarItem(i, price, url, imgUrl, prodName) {
      var title = 'card-link-similar-' + i;
      var img = 'img-card-similar' + i;
      var currentPrice = "#current-price-card-similar" + i;
      //var historyPrice = "#lowest-price-card" + i;
      var name = 'card-title-similar' + i;

      document.getElementById(title).setAttribute("href", url);
      //document.getElementById(footer).setAttribute("href", item.amazonUrl);
      document.getElementById(img).setAttribute("src", imgUrl);
      $(currentPrice).text(price);
      //$(historyPrice).text("$" + item.priceHistory);
      document.getElementById(name).innerHTML = prodName;
    }
	
	var displayLength = 10;
	//console.log(response.similarItemPrice.length);
	if (response.similarItemPrice.length < displayLength) {
		displayLength = response.similarItemPrice.length;
	}
    for (let j = 0; j < displayLength; j++) {
      addSimilarItem(j + 1, response.similarItemPrice[idx[j]], response.similarItemUrl[idx[j]], response.similarImgSrc[idx[j]], response.similarItemName[idx[j]]);
    }


    // Handle possible shipping fee
    var price = response.price.trim();
    var shippingFee = response.shipping.trim();

    // Handle products that cannot be shipped
    if (shippingFee.includes("$")) {
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
    if (productName.includes(",")) {
      productNameShortened = productName.substr(0, productName.indexOf(","));
    }
    document.getElementById('card-title1').innerHTML = productNameShortened;

  });
});

//
