
// Restore status on detail card
// When exitting the modal window by pressing X
$(document).on('click',"[name=detail-modal]",function(e){
	console.log("clicked close on modal");
  if ($(e.target).parent().attr("data-dismiss")) {
	$(this).find("[name=saveThresButton]").prop('disabled', true);
	$(this).find("[name=modifyThresButton]").prop('disabled', false);
	$(this).find("[name=pthres]").prop('readonly', true);
	$(this).find("[name=rate]").prop('disabled', true);
	$(this).find("[name=tthres]").datepicker("destroy");
  }
});

// Enable save, disable modify button
$(document).on('click',"[name=modifyThresButton]",function(){

  //alert('Clicked');
  console.log("clicked modify button");
  var root = $(this).closest("div .modal-content");
  var pthres = root.find("[name=pthres]");
  var rate = root.find("[name=rate]");
  var tthres = root.find("[name=tthres]");
  var saveBtn = root.find("[name=saveThresButton]");
	
  $(this).prop('disabled', true);
  $(pthres).prop('readonly', false);
  $(rate).prop('disabled', false);
  $(saveBtn).prop('disabled', false);
  //thresSave.disabled = false;

  // instantiate the datepicker when modify is clicked
  $(function() {
    $(tthres).datepicker();
  });
});

// Update information
$(document).on('click',"[name=saveThresButton]",function(){
  var root = $(this).closest("div .card");
  var pthres = root.find("[name=pthres]");
  var rate = root.find("[name=rate]");
  var tthres = root.find("[name=tthres]");
  var id = root.find("[name=itemId]");
  //console.log($(id).val());
  //console.log($(tthres).val());
  //console.log($(pthres).val());
  //console.log($(rate).val());
  //console.log($("#tokenId").val());
  var pthresNum = $(pthres).val().substr(1, $(pthres).val().length);

  $.ajax({
    url: "http://localhost:5000/item/update/tracking",
    type: "PUT",
    contentType: "application/json",
    data:JSON.stringify({
      "id": parseInt($(id).val()),
      "timeThreshold": $(tthres).val(),
      "priceThreshold": pthresNum,
      "sampleFrequency": parseInt((rate).val()),
	  "token": $("#tokenId").val()
    }),
    success: function(response, status, xhr) {
      var ct = xhr.getResponseHeader("content-type") || "";
      if (ct.indexOf('html') > -1) {
        alert(response);
      }
      if (ct.indexOf('json') > -1) {
        alert("Successfully updated information.");
		location.reload();
      }
    },
    error: function(xhr) {
      alert("An error occured: " + xhr.status + " " + xhr.statusText);
    }
  });
});

$(document).on('click',"#save-pref-btn",function(){
  //alert("save btn clicked");
  var radios = document.getElementsByName('prime');
  var isPrime = Boolean(false);
  
  if (radios[0].checked) {
    isPrime = Boolean(true);
  } 
  
  $.ajax({
    url: "http://localhost:5000/user/setprime",
    type: "PUT",
    contentType: "application/json",
    data:JSON.stringify({
      "isPrime": isPrime, 
      "token":  $("#tokenId").val()
    }),
	beforeSend: function(xhr) {
      xhr.setRequestHeader("Authorization", $("#tokenId").val());
    },
    success: function(response, status, xhr) {
      var ct = xhr.getResponseHeader("content-type") || "";
      if (ct.indexOf('html') > -1) {
        alert(response);
      }
      if (ct.indexOf('json') > -1) {
        alert("Successfully updated information.");
		location.reload();
      }
    },
    error: function(xhr) {
      alert("An error occured: " + xhr.status + " " + xhr.statusText);
    }
  });
});
