// Mock an object from ajax call
var trackingItem = [];
trackingItem[0] = new TrackingItem("123",                                                                            // id
                                    "Insulated Lunch Bag for Women/Men",                                             // name
									"https://www.amazon.com/dp/B088M93T16/ref=dp_prsubs_1",                          // amazonUrl
									"https://images-na.ssl-images-amazon.com/images/I/61JyAkuhbUL._AC_SL1001_.jpg",  // imgUrl
									"12",                                                                            // priceThreshold
									"10/30/2020",                                                                    // timeThreshold
									"hourly",                                                                        // sampleFrequency
									"12");                                          								 // priceHistory
									
trackingItem[1] = new TrackingItem("124",                                                                            // id
                                    "Yellowstone: Season 2",                                                          // name
									"https://www.amazon.com/Yellowstone-Season-2-Kevin-Costner/dp/B07T1G32SN/ref=pd_sbs_2?pd_rd_w=OviYh&pf_rd_p=b65ee94e-1282-43fc-a8b1-8bf931f6dfab&pf_rd_r=V4E6EYXWKJ4EHQ5FREZB&pd_rd_r=6848917c-ff1c-4e6f-868e-626199d7a0ce&pd_rd_wg=VH4vg&pd_rd_i=B07T1G32SN#",                          // amazonUrl
									"https://images-na.ssl-images-amazon.com/images/I/7110JOVrb9L._SY445_.jpg",      // imgUrl
									"17",                                                                            // priceThreshold
									"10/30/2020",                                                                    // timeThreshold
									"hourly",                                                                        // sampleFrequency
									"15");
console.log(trackingItem);


	addItem(trackingItem[0], 2, "$14.99");
	addItem(trackingItem[1], 3, "$19.95");


function addItem(item, i, price){
   var title = 'card-link-title-' + i;
   //var footer = 'card-link-footer-' + i;
   var img = 'img-card' + i;
   var currentPrice = "#current-price-card" + i;
   var historyPrice = "#lowest-price-card" + i;
   var name = 'card-title' + i;
   
   document.getElementById(title).setAttribute("href", item.amazonUrl);
   //document.getElementById(footer).setAttribute("href", item.amazonUrl);
   document.getElementById(img).setAttribute("src", item.imgUrl);
   $(currentPrice).text(price);
   $(historyPrice).text("$"+item.priceHistory);
   document.getElementById(name).innerHTML = item.name;
}


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

$(function() {
  $("[name=toggler]").click(function() {
    $('.toHide').hide();
    $("#blk-" + $(this).val()).show('slow');
  });
});
