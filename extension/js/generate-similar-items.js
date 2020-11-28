/*
  generate-similar-items.js: dynamically add 10 similar items w/rt their products

*/
console.log("similar-item.js");

var random = 9;

// Page number = number of items / 3
var page = Math.ceil(random / 3);
var cardsLeftover = random;

function addSimilarCard(start, end, page, cardIdx) {
  for (let i = start; i <= end; i++) {
    var card = "<div class=\"card\">";
    card += "      <a href=\"#\" id=\"card-link-similar-" + cardIdx + '-' + i + "\" target=\"_blank\">";
    card += "         <img class=\"card-img-top\" src=\"...\" alt=\"Card image cap\" id = \"img-card-similar" + cardIdx + '-' + i + "\">";
    card += "      </a>";
    card += "      <div class=\"card-body\" style=\"text-align:center\">";
    card += "         <h5 class=\"card-title\" id = \"card-title-similar" + cardIdx + '-' + i + "\">Product Name</h5>";
    card += "         <p class=\"card-text\">";
    card += "            Current Price:";
    card += "            <span class = \"card-price\" id=\"current-price-card-similar" + cardIdx + '-' + i + "\">";
    card += "            ---";
    card += "            </span>";
    card += "            <button type=\"button\" class=\"btn btn-primary\" name=\"register-btn\">Register</button>";
    card += "         </p>";
    card += "      </div>";
    card += "      <div class=\"card-footer\" style=\"text-align:center\">";
    card += "         <small class=\"text-muted\">Last updated 3 mins ago</small>";
    card += "         <button type=\"button\" class=\"btn btn-secondary\" name=\"hide-btn\">Hide this item</button>";
    card += "      </div>";
    card += "   </div>";

    //console.log(card);

    var group = '#card-group-similar' + cardIdx + '-' + page;
	//console.log(group);
    $(card).appendTo(group);
	
  };
}


// add more card page
function addSimilarCardExecution(){
for (let cardIdx = 1; cardIdx < 4; cardIdx++) {
	//console.log("generate-similar.js");
  addSimilarCard(2, 3, 1, cardIdx);
  for (let j = 1; j < 3; j++) {
    $('<div class="carousel-item" id="carousel-item-similar' + cardIdx + '-' + j + '"></div>').appendTo('#carousel-inner-similar-' + cardIdx + '-1' );
    $('<li data-target="#similarItems-' + cardIdx + '" data-slide-to="' + j + '"></li>').appendTo('#carousel-indicators-similar-' + cardIdx);

    // add respective cards
    var cardgroup = j + 1;

    var carouselId = '#carousel-item-similar' + cardIdx + '-' + j;
    //console.log(carouselId);

    $('<div class="card-group" id="card-group-similar' + cardIdx + '-' + cardgroup + '"></div>').appendTo(carouselId);

    
    if (cardsLeftover > 3) {
      var toAdd = cardsLeftover - 3;

      if (toAdd >= 3) {
        addSimilarCard(1 + 3 * j, 3 + 3 * j, cardgroup, cardIdx);
      } else {
        addSimilarCard(1 + 3 * j, toAdd + 3 * j, cardgroup, cardIdx);
      }
      cardsLeftover = cardsLeftover - 3;
    }
  }
  cardsLeftover = 9;
}
}

function sortSimilar(cardIdx, similarItems){
	console.log(cardIdx);
	// Define a holder for items
	var price = [];
	var itemUrl = [];
	var imgUrl = [];
	var name = [];
	
	// Default sort similar items
    var idx = [];
    for (var i = 0; i < similarItems.items.length; i++) {
      idx.push(i);
	  price[i] = similarItems.items[i].price;
	  itemUrl[i] = similarItems.items[i].itemUrl;
	  imgUrl[i] = similarItems.items[i].imgUrl;
	  name[i] = similarItems.items[i].name;
    }
	
    var comparator = function(arr) {
      return function(a, b) {
        var priceA = arr[a];
        var priceB = arr[b];
        priceA = parseFloat(priceA);
        priceB = parseFloat(priceB);
        return priceB > priceA ? 1 : -1;
      };
    };
    idx = idx.sort(comparator(price));
	//console.log(idx);
    //console.log(price);

    var displayLength = price.length;
    
    for (let j = 0; j < displayLength; j++) {
      addSimilarItem(j, price[idx[j]], itemUrl[idx[j]], imgUrl[idx[j]], name[idx[j]], cardIdx);
    }

  }
  
  // Display similar items of a certain product
  function addSimilarItem(i, price, url, imgUrl, prodName, cardIdx) {
	  i += 1;
      var title = '#card-link-similar-' + cardIdx + "-" + i;
      var img = '#img-card-similar' + cardIdx + "-" + i;
      var currentPrice = "#current-price-card-similar" + cardIdx + "-"  + i;
      var name = '#card-title-similar' + cardIdx + "-"  + i;
	  
	  $(title).attr("href", url);
      $(img).attr("src", imgUrl);
      $(currentPrice).text(price);
      $(name).html(prodName);
    }


