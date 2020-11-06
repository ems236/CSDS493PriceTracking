/*
  popup.js: Get similar product lists from the current product page
  
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
      var name = 'card-title-similar' + i;

      document.getElementById(title).setAttribute("href", url);
      document.getElementById(img).setAttribute("src", imgUrl);
      $(currentPrice).text(price);
      document.getElementById(name).innerHTML = prodName;
    }

    var displayLength = 10;
    console.log(response.similarItemPrice.length);
    if (response.similarItemPrice.length < displayLength) {
      displayLength = response.similarItemPrice.length;
    }
    for (let j = 0; j < displayLength; j++) {
      addSimilarItem(j + 1, response.similarItemPrice[idx[j]], response.similarItemUrl[idx[j]], response.similarImgSrc[idx[j]], response.similarItemName[idx[j]]);
    }

  });
});

//
