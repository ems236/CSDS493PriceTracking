/*
  generate-similar-items.js: pre add 10 similar items to tab2

*/
console.log("similar-item.js");
    var random = 10;

    // Page number = number of items / 3
    var page = Math.ceil(random / 3);
    var cardsLeftover = random;

    function addSimilarCard(start, end, page) {
      for (let i = start; i <= end; i++) {
        var card = "<div class=\"card\">";
        card += "      <a href=\"#\" id=\"card-link-similar-" + i + "\" target=\"_blank\">";
        card += "         <img class=\"card-img-top\" src=\"...\" alt=\"Card image cap\" id = \"img-card-similar" + i + "\">";
        card += "      </a>";
        card += "      <div class=\"card-body\" style=\"text-align:center\">";
        card += "         <h5 class=\"card-title\" id = \"card-title-similar" + i + "\">Product Name</h5>";
        card += "         <p class=\"card-text\">";
        card += "            Current Price:";
        card += "            <span class = \"card-price\" id=\"current-price-card-similar" + i + "\">";
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

        var group = '#card-group-similar' + page;
        $(card).appendTo(group);
      };
    }
	
	addSimilarCard(2, 3, 1);


    // add more card page
    for (let j = 1; j < page; j++) {
      $('<div class="carousel-item" id="carousel-item-similar' + j + '"></div>').appendTo('#carousel-inner-similar');
      $('<li data-target="#similarItems" data-slide-to="' + j + '"></li>').appendTo('#carousel-indicators-similar');
      
      // add respective cards
      var cardgroup = j + 1;
      
      var carouselId = '#carousel-item-similar' + j;
	  //console.log(carouselId);
      
	  $('<div class="card-group" id="card-group-similar'+ cardgroup + '"></div>').appendTo(carouselId);
	  
	  
      if (cardsLeftover > 3) {
        var toAdd = cardsLeftover - 3;
        
        if (toAdd >= 3) {
          addSimilarCard(1 + 3 * j, 3 + 3 * j, cardgroup);
        } else {
          addSimilarCard(1 + 3 * j, toAdd + 3 * j, cardgroup);
        }
        cardsLeftover = cardsLeftover - 3;
      }

    }

