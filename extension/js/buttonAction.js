// Click on delete button
$(document).on('click',"[name=delete-btn]",function(){
  //$('[name=cancel-btn]').click();
  
  var root = $(this).closest("div .card");
  var id = root.find("[name=itemId]");
  $.ajax({
    url: "http://localhost:5000/item/delete",
    type: "DELETE",
    contentType: "application/json",
    data: JSON.stringify({
      "id": parseInt($(id).val()), 
	  "token": $("#tokenId").val()
    }),
    success: function(response, status, xhr) {
      var ct = xhr.getResponseHeader("content-type") || "";
      if (ct.indexOf('json') > -1) {
        alert("Removed the product from the list.");
		window.location.reload();
      }
    },
    error: function(xhr) {
      alert("An error occured: " + xhr.status + " " + xhr.statusText);
    }
  });
});

// Click on register button (similar product)
$("[name=register-btn]").on("click", function() {
  var root = $(this).closest("div .card")
  var itemUrl = root.find("a").attr("href");
  var itemUrl = itemUrl.substring(0, itemUrl.indexOf("/ref"));  // Trim item url
  var imgUrl = root.find("img").attr("src");
  var name = root.find(".card-title").text();
  var price = root.find(".card-price").text();
  var price = price.substr(1, price.length);
  
  var referrerRoot = $(this).closest("div .modal").attr('id');
  var cardIdx = referrerRoot.replace("detail-modal-", "");
  var referrerItemId = $("#itemId-" + cardIdx).val();
  //console.log("ReferrerId: "+referrerItemId);
  //console.log(root.find("a").attr("href"));
  //console.log(root.find("img").attr("src"));
  //console.log(root.find(".card-title").text());
  //console.log(root.find(".card-price").text());
  
  
  $.ajax({
    url: "http://localhost:5000/similar/register",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      "itemUrl": itemUrl,
      "imgUrl": imgUrl,
      "name": name,
      "referrerItemId": parseInt(referrerItemId),
      "price": price,
	  "token": $("#tokenId").val()
    }),
    success: function(response, status, xhr) {
      var ct = xhr.getResponseHeader("content-type") || "";
      if (ct.indexOf('html') > -1) {
        alert(response);
      }
      if (ct.indexOf('json') > -1) {
        alert("Successfully registered product.");
      }
    },
    error: function(xhr) {
      alert("An error occured: " + xhr.status + " " + xhr.statusText);
    }
  });*/
});

$("[name=hide-btn]").on("click", function() {
  var root = $(this).closest("div .card");
  
  /*
  $.ajax({
    url: "http://localhost:5000/similar/hide",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      "id": 4,
	  "token": $("#tokenId").val()
    }),
    success: function(response, status, xhr) {
      var ct = xhr.getResponseHeader("content-type") || "";
      if (ct.indexOf('json') > -1) {
        alert("Similar Product is hidden.");
      }
    },
    error: function(xhr) {
      alert("An error occured: " + xhr.status + " " + xhr.statusText);
    }
  });*/
  $(this).closest(".card").remove();
});


// Radio button group for view graph / table

$(document).on('click',"[name=toggler]",function(){
    $('.toHide').hide();
    $("[name=blk-" + $(this).val() + "]").show('slow');
	
	// Display a line chart
	var root = $(this).parent().parent();
	var chLine = root.find("canvas").attr('id');
	//console.log("Which is clicked? " + chLine);
    //var chLine = document.getElementsByName("chLine");
	console.log(chartData);
    if (chLine) {
	  var i = parseInt(chLine.substr(chLine.indexOf("-") + 1, chLine.length));
      new Chart(chLine, {
        type: 'line',
        data: chartData[i],
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: false
              },
              scaleLabel: {
                display: true,
                labelString: 'In $'
              },
            }]
          },
          legend: {
            display: true
          }
        }
      });
    }
	
	//alert("clicked on radio button");
} );

// Radio button group for similar items toggle display

$(document).on('click',"[name=similar]",function(){
	var root = $(this).closest("div .modal").attr('id');
	var cardIdx = root.replace("detail-modal-", "");
	//console.log(cardIdx);
    $('[name=similar_items]').hide();
    var cardgroup = "#card-group-similar" + cardIdx + "-" + $(this).val();
	console.log(cardgroup);
    $(cardgroup).show('slow');
} );
