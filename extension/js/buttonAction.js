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
// TODO: handle referrerItemId
$("[name=register-btn]").on("click", function() {
  var root = $(this).closest("div .card")
  var itemUrl = root.find("a").attr("href");
  var itemUrl = itemUrl.substring(0, itemUrl.indexOf("/ref"));  // Trim item url
  var imgUrl = root.find("img").attr("src");
  var name = root.find(".card-title").text();
  var price = root.find(".card-price").text();
  var price = price.substr(1, price.length);
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
      "referrerItemId": parseInt($("#itemId-1").val()),
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
  });
});

$("[name=hide-btn]").on("click", function() {
  

  /*$.ajax({
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

// chart colors
var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];

/* large line chart */
var chLine = document.getElementById("chLine");
var chartData = {
  labels: ["Nov-1", "Nov-2", "Nov-3", "Nov-4", "Nov-5", "Nov-6", "Nov-7"],
  datasets: [{
      label: "Prime Prices",
      data: [589, 445, 483, 503, 689, 692, 634],
      backgroundColor: 'transparent',
      borderColor: colors[0],
      borderWidth: 4,
      pointBackgroundColor: colors[0]
    },
    {
      label: "Non-Prime Prices",
      data: [639, 465, 493, 524, 735, 760, 674],
      backgroundColor: colors[3],
      borderColor: colors[1],
      borderWidth: 4,
      pointBackgroundColor: colors[1]
    },
    {
      label: "Similar Item 1",
      data: [525, 786, 346, 700, 768, 542, 346],
      backgroundColor: 'transparent',
      borderColor: colors[2],
      borderWidth: 4,
      pointBackgroundColor: colors[2]
    },
    {
      label: "Similar Item 2",
      data: [799, 899, 900, 435, 589, 200, 300],
      backgroundColor: 'transparent',
      borderColor: colors[4],
      borderWidth: 4,
      pointBackgroundColor: colors[4]
    }
  ]
};

if (chLine) {
  new Chart(chLine, {
    type: 'line',
    data: chartData,
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

// Radio button group for view graph / table

$(document).on('click',"[name=toggler]",function(){
    $('.toHide').hide();
    $("[name=blk-" + $(this).val() + "]").show('slow');
	//alert("clicked on radio button");
} );

