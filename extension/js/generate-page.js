/*
  generate-page.js: dynamically adds card to the popup window
                    when information is received.

*/

// chart colors
var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];
var chartData = {};
var similarProds = [];

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
          for (let i = 0; i < prodList.items.length; i++) {
			
            // Filter out the current price
            var currentPrice = "";
            var lowestPrices = [];
            var historyDates = [];
            for (let j = 0; j < prodList.items[i].priceHistory.length; j++) {

              // Handle date format
              var date = new Date(prodList.items[i].priceHistory[j].date);
              var formattedDate = (date.getMonth() + 1) + "/" + date.getDate() + "/" + date.getFullYear();
              var currentDate = new Date();
              var formattedCurrentDate = (currentDate.getMonth() + 1) + "/" + currentDate.getDate() + "/" + currentDate.getFullYear();

              // Save the values
              lowestPrices[j] = prodList.items[i].priceHistory[j].price;
              historyDates[j] = formattedCurrentDate;
              if (formattedDate.toString() === formattedCurrentDate.toString()) {
                currentPrice = "$" + prodList.items[i].priceHistory[j].price;
                //console.log("current price is today's price");
              }

            }
            addItem(i + 1,
              currentPrice,
              prodList.items[i].url,
              prodList.items[i].imgUrl,
              prodList.items[i].title,
              prodList.items[i].priceThreshold,
              prodList.items[i].id,
              prodList.items[i].timeThreshold,
              prodList.items[i].sampleFrequency,
              lowestPrices,
              historyDates
            );
			
			  // Get similar items
              $.ajax({
                url: "http://localhost:5000/dashboard/similaritems",
                type: "GET",
                beforeSend: function(xhr) {
                  xhr.setRequestHeader("Authorization", $("#tokenId").val());
                },
				//contentType: "application/json",
                data: {itemId: parseInt(prodList.items[i].id)},
                success: function(response, status, xhr) {
                  var ct = xhr.getResponseHeader("content-type") || "";
                  if (ct.indexOf('json') > -1) {
                    console.log("Similar products retrieved from the server.");
                    console.log(response);
					similarProds = response;
					sortSimilar(i + 1, similarProds);
                    }
                  },
                
                error: function(xhr) {
                  alert("An error occured: " + xhr.status + " " + xhr.statusText);
                }
              });
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


    var random = 10;

    // Page number = number of items / 3
    var page = Math.ceil(random / 3);
    //alert("This tab has " + page + " pages.");

    var cardsLeftover = random;

    function addCard(start, end, page) {
      for (let i = start; i <= end; i++) {
        var card = "<div class=\"card\" name=\"card\"> ";
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
          '                                      <canvas name="chLine" id="chLine-' + i + '" height="150"></canvas>' +
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
          '                                  </tr>' +
          '                                </thead>' +
          '                                <tbody id= "table-' + i + '">' +
          '                                </tbody>' +
          '                              </table>' +
          '                            </div>' +
		  '                            <div id="similarItems-' + i + '" class="carousel slide" data-ride="carousel" data-interval="false">' +
		  '                              <!-- Indicators -->' +
		  '                              <ul class="carousel-indicators" id="carousel-indicators-similar-' + i + '">' +
		  '                                <li data-target="#similarItems-' + i + '" data-slide-to="0" class="active"></li>' +
		  '                              </ul>' +
		  '                              <!-- The slideshow -->' +
		  '                              <div class="carousel-inner" id="carousel-inner-similar-' + i + '-1">' +
		  '                                <div class="carousel-item active">' + 
		  '                                  <div class="card-group" id="card-group-similar' + i + '-1">' +
		  '                                    <div class="card">' +
		  '                                      <a href="#" id="card-link-similar-' + i + '-1" target="_blank">' +
		  '                                        <img class="card-img-top" src="..." alt="Card image cap" id="img-card-similar' + i + '-1">' +
		  '                                      </a>' +
		  '                                      <div class="card-body" style="text-align:center">' +
		  '                                        <h5 class="card-title" id="card-title-similar' + i + '-1">Card title</h5>' + 
		  '                                        <p class="card-text">' +
		  '                                          Current Price:' +
		  '                                          <span class="card-price" id="current-price-card-similar' + i + '-1">' +
		  '                                            ---' +
		  '                                          </span>' +
		  '                                          <button type="button" class="btn btn-primary" name="register-btn">Register</button>' +
		  '                                      </div>' +
		  '                                      <div class="card-footer" style="text-align:center">' +
		  '                                        <small class="text-muted">Last updated 3 mins ago</small>' +
		  '                                        <button type="button" class="btn btn-secondary" name="hide-btn">Hide this item</button>' +
		  '                                      </div>' +
		  '                                    </div>' +
		  '                                  </div>' +
		  '                                </div>' +
		  '                              </div>' +
		  '                              <!-- Left and right controls -->' +
		  '                              <a class="carousel-control-prev" href="#similarItems-' + i + '" data-slide="prev">' +
		  '                                <span class="carousel-control-prev-icon"></span>' +
		  '                              </a>' +
		  '                              <a class="carousel-control-next" href="#similarItems-' + i + '" data-slide="next">' +
		  '                                <span class="carousel-control-next-icon"></span>' +
		  '                              </a>' +
		  '                            </div>' +
          '                            <p id="p' + i + '">' +
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
          '                            <button type="button" class="btn btn-primary" name="modifyThresButton" id="test' + i + '">Modify Threholds</button>' +
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
	
	addSimilarCardExecution();

    // add more card page
    for (let j = 1; j < page; j++) {
      $('<div class="carousel-item" id="carousel-item-' + j + '"></div>').appendTo('.carousel-inner-item'); 
      $('<li data-target="#demo" data-slide-to="' + j + '"></li>').appendTo('.carousel-indicators-1'); 

      // add respective cards
      var cardgroup = j + 1;
      //console.log("cardgroup: "+cardgroup);
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
    function addItem(i, price, url, imgUrl, prodTitle, priceThreshold, prodId, timeThreshold, sampleFreq, lowestPrice, historyDates) {
      var title = 'card-link-title-' + i;
      var img = 'img-card' + i;
      var currentPrice = "#current-price-card" + i;
      var historyPrice = "#lowest-price-card" + i;
      var name = 'card-title' + i;
      var pthres = "#pthres-" + i;
      var tthres = "#tthres-" + i;
      var rate = "#rate-" + i;
      var id = "#itemId-" + i;
      var table = "#table-" + i;

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
      $(historyPrice).text("$" + min(lowestPrice));
      $(id).val(prodId);
      document.getElementById(name).innerHTML = prodTitle;


      for (let j = 0; j < historyDates.length; j++) {

        // Fill in the graphs 
        var chartData_toAdd = {};
        if (j == 0) { // First object: initialize the object fields
          chartData_toAdd = {
            [i]: {
              labels: [],
              datasets: [{
                  label: "Prime Prices",
                  data: [],
                  backgroundColor: 'transparent',
                  borderColor: colors[0],
                  borderWidth: 4,
                  pointBackgroundColor: colors[0]
                },
                {
                  label: "Non-Prime Prices",
                  data: [],
                  backgroundColor: colors[3],
                  borderColor: colors[1],
                  borderWidth: 4,
                  pointBackgroundColor: colors[1]
                }
              ]
            }
          }
        } else { // Keep the previous object information 
          chartData_toAdd = {
            [i]: {
              labels: chartData[i].labels,
              datasets: [{
                  label: "Prime Prices",
                  data: chartData[i].datasets[0].data,
                  backgroundColor: 'transparent',
                  borderColor: colors[0],
                  borderWidth: 4,
                  pointBackgroundColor: colors[0]
                },
                {
                  label: "Non-Prime Prices",
                  data: chartData[i].datasets[1].data,
                  backgroundColor: colors[3],
                  borderColor: colors[1],
                  borderWidth: 4,
                  pointBackgroundColor: colors[1]
                }
              ]
            }
          };
        }

        chartData_toAdd[i].labels[j] = historyDates[j];
        chartData_toAdd[i].datasets[0].data[j] = lowestPrice[j];
        chartData_toAdd[i].datasets[1].data[j] = lowestPrice[j];

        $.extend(chartData, chartData_toAdd);

        //console.log(chartData);

        // Fill in the tables
        var row = '<tr>' +
          '  <th scope="row">' + historyDates[j] + '</th>' +
          '  <td>' + "$" + lowestPrice[j] + '</td>' +
          '</tr>';
        $(table).append(row);
      }


    }

    // Get min value from an array
    function min(input) {
      if (toString.call(input) !== "[object Array]")
        return false;
      return Math.min.apply(null, input);
    }

  }
});
