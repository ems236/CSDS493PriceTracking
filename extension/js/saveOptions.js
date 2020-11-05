var thresModify = document.getElementById("modifyThresButton");
var thresSave = document.getElementById("saveThresButton");

// Restore modify and save button status on detail card
// When exitting the modal window by pressing X
$('#detailModal').on('click', function(e) {
  if ($(e.target).parent().attr("data-dismiss")) {
    thresModify.disabled = false;
    thresSave.disabled = true;
  }
});

// Enable save, disable modify button
$("#modifyThresButton").click(function() {
  $("#pthres").prop('readonly', false);
  thresModify.disabled = true;
  thresSave.disabled = false;

  // instantiate the datepicker when modify is clicked
  $(function() {
    $("#tthres").datepicker();
  });

});
