document.addEventListener("deviceready", onDeviceReady, false);

function onDeviceReady() {
	document.getElementById("infoField").innerHTML = "Thanh Hai Nguyen";
	deviceInfoApp = new deviceInfoApp();
	deviceInfoApp.run();
	
}

function deviceInfoApp() {
}

deviceInfoApp.prototype = {
    
	run:function() {
		var that = this;
		document.getElementById("deviceName").addEventListener("click", function() {
			that._viewDeviceName.apply(that, arguments);
		});
		document.getElementById("deviceCordovaVersion").addEventListener("click", function() {
			that._viewCordovaVersion.apply(that, arguments);
		});
		document.getElementById("devicePlatform").addEventListener("click", function() {
			that._viewDevicePlatform.apply(that, arguments);
		});
		document.getElementById("deviceUUID").addEventListener("click", function() {
			that._viewDeviceUUID.apply(that, arguments);
		});
		document.getElementById("deviceVersion").addEventListener("click", function() {
			that._viewDeviceVersion.apply(that, arguments);
		});
		document.getElementById("geoLocation").addEventListener("click", function() {
			that._viewGeoLocation.apply(that, arguments);
		});
	},
    
	_viewDeviceName : function() {
		var infoField = document.getElementById("infoField");
		infoField.innerHTML = device.model;
	},
    
	_viewCordovaVersion : function() {
		var infoField = document.getElementById("infoField");
		infoField.innerHTML = device.cordova;
	},
    
	_viewDevicePlatform : function () {
		var infoField = document.getElementById("infoField");
		infoField.innerHTML = device.platform;
	},
    
	_viewDeviceUUID : function () {
		var infoField = document.getElementById("infoField");
		infoField.innerHTML = device.uuid;
	},
    
	_viewDeviceVersion:function viewDeviceVersion() {
		var infoField = document.getElementById("infoField");
		infoField.innerHTML = device.version;
	},
	
	_viewGeoLocation:function viewGeoLocation() {
		var infoField = document.getElementById("infoField");
		navigator.geolocation.getCurrentPosition(onSuccess, onError);
		//onSuccess Geolocation
		//
		function onSuccess(position) {
			var infoField = document.getElementById("infoField");
			infoField.innerHTML = 'Latitude: '           + position.coords.latitude              + '<br />' +
		                        'Longitude: '          + position.coords.longitude             + '<br />' +
		                        'Altitude: '           + position.coords.altitude              + '<br />' +
		                        'Accuracy: '           + position.coords.accuracy              + '<br />' +
		                        'Altitude Accuracy: '  + position.coords.altitudeAccuracy      + '<br />' +
		                        'Timestamp: '          + position.timestamp                    + '<br />';
		}

		// onError Callback receives a PositionError object
		//
		function onError(error) {
		    alert('code: '    + error.code    + '\n' +
		          'message: ' + error.message + '\n');
		}
	}
	
};
