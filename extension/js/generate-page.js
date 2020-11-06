/*
  generate-page.js: dynamically adds card to the popup window
                    when information is received.

*/



// Get token and save the value
chrome.runtime.sendMessage({
  message: 'login'
}, function(response) {
  if (response.success) {

    $("#tokenId").val(response.token);

    // Get item list from the server
    var prodList;
    $.ajax({
      url: "http://localhost:5000/dashboard/list",
      type: "GET",
      beforeSend: function(xhr) {
        xhr.setRequestHeader("Authorization", $("#tokenId").val());
      },
      //contentType: "application/json",
      //data: {"token": $("#tokenId").val()},
      //headers: {"token": $("#tokenId").val()},
      success: function(response, status, xhr) {
        var ct = xhr.getResponseHeader("content-type") || "";
        if (ct.indexOf('json') > -1) {
          console.log("Products retrieved from the server.");
          console.log(response);
          prodList = response;
          //console.log(prodList.items[0].id);
          //prodList = response;
		  for (let i = 0; i < prodList.items.length; i++){
			  addItem(i+1, 
			          "$23.99", 
					  prodList.items[i].url, 
					  prodList.items[i].imgUrl, 
					  prodList.items[i].title, 
					  prodList.items[i].priceThreshold, 
					  prodList.items[i].id, 
					  prodList.items[i].timeThreshold, 
					  prodList.items[i].sampleFrequency);
		  }
          
        }
      },
      error: function(xhr) {
        alert("An error occured: " + xhr.status + " " + xhr.statusText);
      }
    });
	
	// Get prime status from the server
	$.ajax({
    url: "http://localhost:5000/user/isprime",
    type: "GET",
    beforeSend: function(xhr) {
      xhr.setRequestHeader("Authorization", $("#tokenId").val());
    },
    success: function(response, status, xhr) {
      var ct = xhr.getResponseHeader("content-type") || "";
      if (ct.indexOf('json') > -1) {
		console.log(response);
		if (response.isPrime) {
			$("#isPrime").prop('checked', true);
		} else {
			$("#isNotPrime").prop('checked', true);
		}
      }
    },
    error: function(xhr) {
      alert("An error occured: " + xhr.status + " " + xhr.statusText);
    }
  });



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
		card += "     <input type=\"hidden\" name=\"itemId\" id=\"itemId-" + i + "\">"
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
        card += "         <a data-toggle=\"modal\" href=\"#detail-modal-" + i + "\" class=\"card-link\" id=\"card-link-footer-" + i + "\">Detail</a>";

        card += '         <!-- Modal for detail -->' +
          '                    <div class="modal fade" name="detail-modal" id="detail-modal-' + i + '" tabindex="-1" role="dialog" aria-labelledby="ModalTitle" aria-hidden="true">' +
          '                      <div class="modal-dialog" role="document">' +
          '                        <div class="modal-content">' +
          '                          <div class="modal-header">' +
          '                            <h5 class="modal-title">Detail</h5>' +
          '                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
          '                              <span aria-hidden="true">&times;</span>' +
          '                            </button>' +
          '                          </div>' +
          '                          <div class="modal-body">' +
          '                            <label><input type="radio" name="toggler" value="1" />View Graph</label>' +
          '                            <label><input type="radio" name="toggler" value="2" />View Table</label>' +
          '                            <div name="blk-1" class="toHide" style="display:none">' +
          '                              <div class="row my-3">' +
          '                                <div class="col">' +
          '                                  <h4>Price History</h4>' +
          '                                </div>' +
          '                              </div>' +
          '                              <div class="row my-2">' +
          '                                <div class="col-md-12">' +
          '                                  <div class="card">' +
          '                                    <div class="card-body">' +
          '                                      <canvas id="chLine" height="150"></canvas>' +
          '                                    </div>' +
          '                                  </div>' +
          '                                </div>' +
          '                              </div>' +
          '                            </div>' +
          '                            <div name="blk-2" class="toHide" style="display:none">' +
          '                              <table class="table">' +
          '                                <thead class="thead-dark">' +
          '                                  <tr>' +
          '                                    <th scope="col">Date</th>' +
          '                                    <th scope="col">Item</th>' +
          '                                    <th scope="col">Similar Item 1</th>' +
          '                                    <th scope="col">Similar Item 2</th>' +
          '                                  </tr>' +
          '                                </thead>' +
          '                                <tbody>' +
          '                                  <tr>' +
          '                                    <th scope="row">Nov-1</th>' +
          '                                    <td>$639</td>' +
          '                                    <td>$525</td>' +
          '                                    <td>$799</td>' +
          '                                  </tr>' +
          '                                  <tr>' +
          '                                    <th scope="row">Nov-2</th>' +
          '                                    <td>$465</td>' +
          '                                    <td>$786</td>' +
          '                                    <td>$899</td>' +
          '                                  </tr>' +
          '                                  <tr>' +
          '                                    <th scope="row">Nov-3</th>' +
          '                                    <td>$493</td>' +
          '                                    <td>$346</td>' +
          '                                    <td>$900</td>' +
          '                                  </tr>' +
          '                                  <tr>' +
          '                                    <th scope="row">Nov-4</th>' +
          '                                    <td>$524</td>' +
          '                                    <td>$700</td>' +
          '                                    <td>$435</td>' +
          '                                  </tr>' +
          '                                  <tr>' +
          '                                    <th scope="row">Nov-5</th>' +
          '                                    <td>$735</td>' +
          '                                    <td>$768</td>' +
          '                                    <td>$589</td>' +
          '                                  </tr>' +
          '                                  <tr>' +
          '                                    <th scope="row">Nov-6</th>' +
          '                                    <td>$760</td>' +
          '                                    <td>$542</td>' +
          '                                    <td>$200</td>' +
          '                                  </tr>' +
          '                                  <tr>' +
          '                                    <th scope="row">Nov-7</th>' +
          '                                    <td>$674</td>' +
          '                                    <td>$346</td>' +
          '                                    <td>$300</td>' +
          '                                  </tr>' +
          '                                </tbody>' +
          '                              </table>' +
          '                            </div>' +
          '                            <p>' +
          '                              Price Threshold:' +
          '                              <input type="text" name="pthres" id="pthres-' + i + '" value="$100" readonly="true" />' +
          '                            </p>' +
          '                            <p>' +
          '                              Time Threshold:' +
          '                              <input type="text" name="tthres" id="tthres-' + i + '" value="11/10/2020" readonly="true" />' +
          '                            </p>' +
          '' +
          '                            <p>' +
          '                              Sample Frequency:' +
          '                              <select name="rate" id="rate-' + i + '" disabled>' +
          '                                <option value="1">Hourly</option>' +
          '                                <option value="2">Daily</option>' +
          '                                <option value="3">Monthly</option>' +
          '                              </select>' +
          '                            </p>' +
          '' +
          '                          </div>' +
          '                          <div class="modal-footer">' +
          '                            <button type="button" class="btn btn-primary" name="modifyThresButton" id="test'+i+'">Modify Threholds</button>' +
          '                            <button type="button" class="btn btn-primary" name="saveThresButton" disabled>Save</button>' +
          '                          </div>' +
          '                        </div>' +
          '                      </div>' +
          '                    </div>';

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
      $('<li data-target="#demo" data-slide-to="' + j + '"></li>').appendTo('.carousel-indicators'); // should be id

      // add respective cards
      var cardgroup = j + 1;
      console.log(cardgroup);
      var carouselId = '#carousel-item-' + j;

      $('<div class="card-group" id="card-group-' + cardgroup + '"></div>').appendTo(carouselId);


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

    // Add item information to the cards
    function addItem(i, price, url, imgUrl, prodTitle, priceThreshold, prodId, timeThreshold, sampleFreq) {
      var title = 'card-link-title-' + i;
      var img = 'img-card' + i;
      var currentPrice = "#current-price-card" + i;
      //var historyPrice = "#lowest-price-card" + i;
      var name = 'card-title' + i;
	  var pthres = "#pthres-" + i;
	  var tthres = "#tthres-" + i;
	  var rate = "#rate-" + i;
	  var id = "#itemId-" + i; 
	  
	  // Handle date format
	  var date = new Date(timeThreshold);
	  var formattedDate = (date.getMonth() + 1) + "/" + date.getDate() + "/" + date.getFullYear();
	  
	  // Assign values
      document.getElementById(title).setAttribute("href", url);
      document.getElementById(img).setAttribute("src", imgUrl);
      $(currentPrice).text(price);
	  $(pthres).attr('value', "$" + priceThreshold);
	  $(tthres).attr('value', formattedDate);
	  $(rate).val(sampleFreq);
      //$(historyPrice).text("$" + prodList.items[i-1].priceThreshold);
	  $(id).val(prodId);
      document.getElementById(name).innerHTML = prodTitle;
    }

  }
});
