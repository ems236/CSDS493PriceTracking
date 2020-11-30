$.ajax({
	url: "http://localhost:5000/notify/items",
	type: 'GET', 
	dataType: 'json',
	success: function(response) {
        var objects = response.items
        // send a message for chrome notification for each item
		for (var i = 0; i < objects.length; i++) {
			var obj_title = objects[0].title
			console.log(obj_title)
			chrome.runtime.sendMessage('', {
				type: 'notification',
				options: {
					title: "Amazon Price Tracking Notification",
					message: obj_title + " reached your threshold",
					iconUrl: "images/icon32.png",
					type: "basic"
				}
			});
		}
	},
	failure: function (response) {
		console.log("Failure to get items")
	}
});