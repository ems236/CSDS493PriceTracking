/*
  inject.js: inject InjectedContentUI.html to the product's page
  
  TODO: location may have surprising difference
*/
$.get(chrome.runtime.getURL('InjectedContentUI.html'), function(data) {
    // This location can be changing 
    // Check if the track button actually gets injected
    if($('#exports_desktop_qualifiedBuybox_atc_feature_div').length)
    {
      $("#exports_desktop_qualifiedBuybox_atc_feature_div").before(data);
      console.log('Price track button injected.');
    }
});	


