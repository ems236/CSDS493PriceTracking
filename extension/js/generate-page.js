/*
  generate-page.js: dynamically adds card to the popup window
                    when information is received.

  TODO: should be handling information from the backend
*/

    //Randomly generates carousel item based on the amount of card items
    var random = 3;
    //alert("This tab has " + random + " card items.");

    // Page number = number of items / 3
    var page = Math.ceil(random / 3);
    //alert("This tab has " + page + " pages.");

    var cardsLeftover = random;

    function addCard(start, end, page) {
      for (let i = start; i <= end; i++) {
        var card = "<div class=\"card\">";
        card += "      <a href=\"#\" id=\"card-link-title-" + i + "\" target=\"_blank\">";
        card += "         <img class=\"card-img-top\" src=\"...\" alt=\"Card image cap\" id = \"img-card" + i + "\">";
        card += "      </a>";
        card += "      <div class=\"card-body\" style=\"text-align:center\">";
        card += "         <h5 class=\"card-title\" id = \"card-title" + i + "\">Product Name</h5>";
        card += "         <p class=\"card-text\">";
        card += "            Current Price:";
        card += "            <span class = \"card-price\" id=\"current-price-card" + i + "\">";
        card += "            ---";
        card += "            </span>";
        card += "            Lowest Price:";
        card += "            <span id=\"lowest-price-card" + i + "\">";
        card += "            ---";
        card += "            </span>";
        card += "            <h6>Shipping included, if any</h6>";
        card += "         </p>";
	card += "         <!-- trigger modal -->";
        card += "         <a data-toggle=\"modal\" href=\"#detailModal\" class=\"card-link\" id=\"card-link-footer-"+ i + "\">Detail</a>";
	card += "         <p></p>";
	card += "         <a data-toggle=\"modal\" href=\"#deleteModal-" + i + "\" class=\"card-link\" id=\"card-link-delete-" + i + "\">Delete</a>";
	card += "         <!-- Modal for delete-->";
	card += "         <div class=\"modal\" id=\"deleteModal-" + i + "\" tabindex=\"-1\" role=\"dialog\" aria-hidden=\"true\">";
	card += "           <div class=\"modal-dialog\" role=\"document\">";
	card += "             <div class=\"modal-content\">";
	card += "               <div class=\"modal-header\">";
	card += "                 <h5 class=\"modal-title\">Confirm delete</h5>";
	card += "                 <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">";
	card += "                   <span aria-hidden=\"true\">&times;</span>";
	card += "                 </button>";
	card += "               </div>";
	card += "               <div class=\"modal-body\">";
	card += "                 <p>Delete this item from the product list?</p>";
	card += "               </div>";
	card += "               <div class=\"modal-footer\">";
	card += "                 <button type=\"button\" class=\"btn btn-primary\" name=\"delete-btn\">Delete</button>";
	card += "                 <button type=\"button\" class=\"btn btn-secondary\" name=\"cancel-btn\" data-dismiss=\"modal\">Cancel</button>";
	card += "               </div>";
	card += "             </div>";
	card += "           </div>";
	card += "         </div>";
        card += "      </div>";
        card += "      <div class=\"card-footer\" style=\"text-align:center\">";
        card += "         <small class=\"text-muted\">Last updated 3 mins ago</small>";
        card += "      </div>";
        card += "   </div>";

        var group = '#card-group-' + page;
        $(card).appendTo(group);
      };
    }

    // first card tab add two cards
	if (random > 1 && random <= 3) {
		addCard(2, random, 1);
	} else if (random > 3) {
		addCard(2, 3, 1);
	}
    

    // add more card page
    for (let j = 1; j < page; j++) {
      $('<div class="carousel-item" id="carousel-item-' + j + '"></div>').appendTo('.carousel-inner'); // shouuld be id
      $('<li data-target="#demo" data-slide-to="' + j + '"></li>').appendTo('.carousel-indicators');  // should be id
      
      // add respective cards
      var cardgroup = j + 1;
      console.log(cardgroup);
      var carouselId = '#carousel-item-' + j;
      
	  $('<div class="card-group" id="card-group-'+ cardgroup + '"></div>').appendTo(carouselId);
	  
	  
      if (cardsLeftover > 3) {
        var toAdd = cardsLeftover - 3;
        
        if (toAdd >= 3) {
          addCard(1 + 3 * j, 3 + 3 * j, cardgroup);
        } else {
          addCard(1 + 3 * j, toAdd + 3 * j, cardgroup);
        }
        cardsLeftover = cardsLeftover - 3;
      }

    }
	
	
