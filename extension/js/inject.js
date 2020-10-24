/*
  inject.js: inject InjectedContentUI.html to the product's page
  
  TODO: location may have surprising difference
*/
$.get(chrome.runtime.getURL('InjectedContentUI.html'), function(data) {
    $("#addToCart_feature_div").before(data);
});	

console.log('Price track button injected.');
