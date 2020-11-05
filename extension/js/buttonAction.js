// Click on delete button
// TODO: send delete request
$("[name=delete-btn]").on("click", function() {
  $('[name=cancel-btn]').click();
  $(this).closest(".card").remove();
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
  console.log(JSON.stringify({
      "itemUrl": itemUrl,
      "imgUrl": imgUrl,
      "name": name,
      "referrerItemId": 1,
      "price": price
    }));
  
  $.ajax({
    url: "http://localhost:5000/similar/register",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      "itemUrl": itemUrl,
      "imgUrl": imgUrl,
      "name": name,
      "referrerItemId": 1,
      "price": price
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
  $(this).closest(".card").remove();
  
  /*
  $.ajax({
    url: "http://localhost:5000/similar/hide",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      "id": "id"
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
