chrome.alarms.create("notificationAlarm", {periodInMinutes: 1});
console.log("alarm set");



function pollNotifications(token)
{
	$.ajax({
		url: "http://localhost:5000/notify/items",
		type: 'GET', 
		dataType: 'json',
		beforeSend: function(xhr) {
			xhr.setRequestHeader("Authorization", token);
		},
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
}

chrome.alarms.onAlarm.addListener(function (alarm) {
	console.log("Alarm fired");
	lookupToken(
		function(token)
		{
			console.log("got token");
			pollNotifications(token);
		},
		function()
		{
			console.log("token failed in notifications");
		}
	)
});
