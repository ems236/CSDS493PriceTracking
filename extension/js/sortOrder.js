
$(document).ready(function() {
	
  // Make the cards draggable
  $("#card-group-1").sortable();
  $("#card-group-1").disableSelection();
  $("#card-group-2").sortable();
  $("#card-group-2").disableSelection();
  $("#card-group-3").sortable();
  $("#card-group-3").disableSelection();
  
});

// Sort the cards by a certain order
// Triggered on change
$("#sort-order").change(function() {
  triggerSort();
});

$("#sort-order-asc-desc").change(function() {
  triggerSort();
});

// Sort the cards asc or desc
function triggerSort() {
  sortByOrder($("#sort-order-asc-desc").val());
}

// Sort based on the sort order
// order: 1 - descending
//        2 - ascending
function sortByOrder(order) {
	//lert($('#card-group-1 [name=card]').length);
  $('#card-group-1 [name=card]').sort(function(a, b) {

    // Sort by price
    if ($("#sort-order").val() == "1") {
      var priceA = $(a).find(".card-price").text();
      var priceB = $(b).find(".card-price").text();

      if (order == "1") {
        return priceB.substr(1, priceB.length) > priceA.substr(1, priceA.length) ? 1 : -1;
      } else {
        return priceA.substr(1, priceA.length) > priceB.substr(1, priceB.length) ? 1 : -1;
      }

    }
    // Sort by product name
    else if ($("#sort-order").val() == "2") {

      if (order == "1") {
        return $(b).find(".card-title").text() > $(a).find(".card-title").text() ? 1 : -1;
      } else {
        return $(a).find(".card-title").text() > $(b).find(".card-title").text() ? 1 : -1;
      }

    }
    // Sort by time threshold
    else if ($("#sort-order").val() == "3") {
	  if (order == "1") {
		//return new Date($(b).find("[name=tthres]").val().date) - new Date($(a).find("[name=tthres]").val().date);
        return new Date($(b).find("[name=tthres]").val().date) > new Date($(a).find("[name=tthres]").val().date) ? 1 : -1;
      } else {
        return new Date($(a).find("[name=tthres]").val().date) > new Date($(b).find("[name=tthres]").val().date) ? 1 : -1;
      }
      
    }
  }).appendTo("#card-group-1");
}




