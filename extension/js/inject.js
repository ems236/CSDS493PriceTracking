/*
  inject.js: inject InjectedContentUI.html to the product's page
  
  TODO: location may have surprising difference
*/

chrome.runtime.sendMessage({
  message: 'login'
}, function(response) {
  if (response.success) {
    //console.log(response.token);
    $.get(chrome.runtime.getURL('InjectedContentUI.html'), function(data) {
      // This location can be changing 
      // Check if the track button actually gets injected
	  data += '<input type="hidden" id="tokenId" name="tokenId" value="' + response.token + '">';
      if ($('#exports_desktop_qualifiedBuybox_atc_feature_div').length) {
        $("#exports_desktop_qualifiedBuybox_atc_feature_div").before(data);
        console.log('Price track button injected.');
      }
    });
  }
});
