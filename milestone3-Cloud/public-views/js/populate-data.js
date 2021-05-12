$(document).ready(() => {
	// if deployed to a site supporting SSL, use wss://
	const protocol = document.location.protocol.startsWith('https') ? 'wss://' : 'ws://';
	const webSocket = new WebSocket(protocol + location.host);
	console.log('URL: ', protocol + location.host);
	// Led 1
	$(function () {
		$('#toggle-status1').bootstrapToggle({
			on: 'On',
			off: 'Off'
		});
	});

	$(function () {
		$('#toggle-status1').change(function () {
			sendAction('_turnOnOff', '1', $(this).prop('checked'));
		});
	});
	// Led 2
	$(function () {
		$('#toggle-status2').change(function () {
			sendAction('_turnOnOff', '2', $(this).prop('checked'));
		});
	});

	$(function () {
		$('#toggle-status2').bootstrapToggle({
			on: 'On',
			off: 'Off'
		});
	});

	// A class for holding the last N points of telemetry for a device
	class DeviceData {
		constructor(deviceId) {
			this.deviceId = deviceId;
			this.maxLen = 100;
			this.timeData = new Array(this.maxLen);
			this.IotData = new Array(this.maxLen);
			this.temperatureData = new Array(this.maxLen);
			this.humidityData = new Array(this.maxLen);
			this.ultraData = new Array(this.maxLen);
			this.blinkLedData = new Array(this.maxLen);
			this.led1Data = new Array(this.maxLen);
			this.led2Data = new Array(this.maxLen);
		}

		addData({ iotData, time, temperature, humidity, ultra, blinkled, led1, led2 }) {
			this.IotData.push(iotData);
			this.timeData.push(time);
			this.temperatureData.push(temperature || null);
			this.humidityData.push(humidity || null);
			this.ultraData.push(ultra || null);
			this.blinkLedData.push(blinkled || null);
			this.led1Data.push(led1 || null);
			this.led2Data.push(led2 || null);

			if (this.timeData.length > this.maxLen) {
				this.IotData.shift();
				this.timeData.shift();
				this.temperatureData.shift();
				this.humidityData.shift();
				this.ultraData.shift();
				this.blinkLedData.shift();
				this.led1Data.shift();
				this.led2Data.shift();
			}
		}
	}

	// All the devices in the list (those that have been sending telemetry)
	class TrackedDevices {
		constructor() {
			this.devices = [];
		}

		// Find a device based on its Id
		findDevice(deviceId) {
			for (let i = 0; i < this.devices.length; ++i) {
				if (this.devices[i].deviceId === deviceId) {
					return this.devices[i];
				}
			}

			return undefined;
		}

		getDevicesCount() {
			return this.devices.length;
		}
	}


	let needsAutoSelect = true;
	const trackedDevices = new TrackedDevices();
	const deviceCount = document.getElementById('deviceCount');
	const listOfDevices = document.getElementById('listOfDevices');

	function OnSelectionChange() {
		const device = trackedDevices.findDevice(listOfDevices[listOfDevices.selectedIndex].text);
		console.log("onSelectionChange: ", device)
		changeViewToDevice(device);
	}

	function changeViewToDevice(device) {
		// last update
		$('#table-caption-update-value').html(device.timeData.slice(-1)[0]); // last element
		$('#table-caption-device-value').html(device.deviceId);
		var deviceData = device.IotData.slice(-1)[0];

		$('#response pre').html(JSON.stringify(deviceData));
		$('#table-temperature-value').html(deviceData.temperature);
		$('#table-humidity-value').html(deviceData.humidity);
		$('#table-ultra-value').html(deviceData.ultra);

		$('#table-led-blink-value').html(deviceData.blinkingLed);
		$('#table-led1-value').html(deviceData.led1 === true ? 'on' : 'off');
		$('#table-led2-value').html(deviceData.led2 === true ? 'on' : 'off');
	}

	listOfDevices.addEventListener('change', OnSelectionChange, false);

	webSocket.onmessage = function onMessage(message) {
		try {
			const messageData = JSON.parse(message.data);
			console.log('onmessage', messageData);

			// find or add device to list of tracked devices
			const existingDeviceData = trackedDevices.findDevice(messageData.DeviceId);

			if (!existingDeviceData) {
				const newDeviceData = new DeviceData(messageData.DeviceId);
				trackedDevices.devices.push(newDeviceData);
				const numDevices = trackedDevices.getDevicesCount();
				deviceCount.innerText = numDevices === 1 ? `${numDevices} device` : `${numDevices} devices`;

				// make data entry
				addDataEntry(newDeviceData, messageData);

				// add device to the UI list
				const node = document.createElement('option');
				const nodeText = document.createTextNode(messageData.DeviceId);
				node.appendChild(nodeText);
				listOfDevices.appendChild(node);

				// if this is the first device being discovered, auto-select it
				if (needsAutoSelect) {
					needsAutoSelect = false;
					listOfDevices.selectedIndex = 0;
					OnSelectionChange();
				}
			} else {
				// make data entry
				addDataEntry(existingDeviceData, messageData);
			}

			// make a new entry in the log.
			writeTolog(messageData);

			// Check if selected is equal to received update accordingly.
			if (messageData.DeviceId === getSelectedDeviceID()) {
				updateView(messageData);
			}
		} catch (err) {
			console.error('eRRor ', err);
		}
	};

	function getSelectedDeviceID() {
		return listOfDevices[listOfDevices.selectedIndex].text;
	}

	function addDataEntry(deviceData, dataToAdd) {
		// https://medium.com/dailyjs/named-and-optional-arguments-in-javascript-using-es6-destructuring-292a683d5b4e

		deviceData.addData({
			iotData: dataToAdd.IotData,
			time: dataToAdd.MessageDate,
			temperature: dataToAdd.IotData.temperature,
			humidity: dataToAdd.IotData.humidity,
			ultra: dataToAdd.IotData.ultra,
			blinkled: dataToAdd.IotData.blinkingLed,
			led1: dataToAdd.IotData.led1,
			led2: dataToAdd.IotData.led2
		});
	}

	function updateView(data) {
		// last update
		$('#table-caption-update-value').html(data.MessageDate);
		$('#table-caption-device-value').html(data.DeviceId);
		var deviceData = data.IotData;

		$('#response pre').html(JSON.stringify(data.IotData));
		$('#table-temperature-value').html(deviceData.temperature);
		$('#table-humidity-value').html(deviceData.humidity);
		$('#table-ultra-value').html(deviceData.ultra);

		$('#table-led-blink-value').html(deviceData.blinkingLed);
		$('#table-led1-value').html(deviceData.led1 === true ? 'on' : 'off');
		$('#table-led2-value').html(deviceData.led2 === true ? 'on' : 'off');
	}

	function sendAction(type, lednum, paramvalue) {
		console.log('You called sendAction(' + type + ', ' + paramvalue + ')');
		var dataToSend = JSON.stringify({ deviceId: getSelectedDeviceID(), ledNumber: lednum, value: paramvalue });
		console.log('SENDING DATA: ', dataToSend);

		webSocket.send(dataToSend);
		// update view this instance.
		$('#table-led' + lednum + '-value').html(paramvalue === true ? 'on' : 'off');
	}


	function writeTolog(data) {
		console.log("writeToLog.data: ", data);
		var table = document.getElementById('logTable');

		table === null ? console.log("table null") : null;
		var row = table.insertRow(1);
		var cell1 = row.insertCell(0);

		var cell2 = row.insertCell(1);
		var cell3 = row.insertCell(2);
		cell1.className = "col-xs-3";
		var b = document.createElement('b');
		b.innerHTML = data.DeviceId;
		cell1.appendChild(b);

		cell2.className = "col-xs-3";
		cell2.innerHTML = data.MessageDate

		cell3.className = "col-xs-6";
		cell3.innerHTML = JSON.stringify(data.IotData, null, 2);
	}





});

