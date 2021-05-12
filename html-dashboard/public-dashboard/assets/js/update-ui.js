const BIC = 'BIC';
const WIN = 'WIN';
const CR = "CR";
const TEAM_HOME = "HOME";
const TEAM_AWAY = "AWAY";
const RESET_BOARD = "RESET_BOARD";
const START_BOARD = "START_BOARD";
const STOP_BOARD = "STOP_BOARD";
const FSR = "fsr";
const OPEN_CV = "opencv"

let TEAM_HOME_NAME;
let TEAM_AWAY_NAME;
let HOME_CUPS;
let AWAY_CUPS;


let deviceID = null

$(document).ready(() => {
	populateScoreboard()
	const protocol = document.location.protocol.startsWith('https') ? 'wss://' : 'ws://';
	const webSocket = new WebSocket(protocol + location.host);
	console.log('URL: ', protocol + location.host);

	webSocket.onmessage = function onMessage(message) {
		try {
			const messageData = JSON.parse(message.data);
			console.log('--> onmessage:::', messageData);
			deviceID = messageData.DeviceId;
			var body = messageData.IotData
			var eventtype = body.eventtype;
			switch (eventtype) {
				case BIC:
					// code block
					showNotification(body.team, body.score);
					break;
				case WIN:
					// code block
					updateToShowWinner(body.team)
					break;
				case CR:
					// code block
					updateScoreBoard(body.team, body.score)
					break;
				default:
					// code block
					console.error("We received an event we were not able to handle.")
					break;
			}

			
		} catch (err) {
			console.error('ERROR ', err);
		}
	};

	function updateScoreBoard(team, newScore){
		

		if (team == TEAM_HOME){
			$( "#home-cups-left" ).html(newScore);

		}else if (team == TEAM_AWAY){
			$( "#away-cups-left" ).html(newScore);
		} else {
			console.error("Wrong team recieved")
		}

		
	}

	function updateToShowWinner(winnerTeam){

		// TODO: !!!! Should we do something funky?

		$.notify(
		{
				icon: 'nc-icon nc-bell-55',
				// icon: 'glyphicon glyphicon-bullhorn',
				message: 'Team: <strong>' + convertTeamToName(winnerTeam) + '</strong> won!'
		},
		{
			allow_dismiss: true,
			type: 'info',
			timer: 5000,
			placement: {
				from: 'bottom',
				// from: 'top',
				align: 'center'
			},
			// animate: {
			// 	enter: 'animated rollIn',
			// 	exit: 'animated rollOut'
			// },
		});

		
		$( "#away-col" ).css("background-color", "rgb(" + 13+ "," +207+","+ 13+ ")"); // rgb(13, 207, 13)
		$( "#home-col" ).css("background-color", "rgb(" + 207+ "," +26+","+ 26+ ")"); // rgb(207, 26, 26)

		// setTimeout(function() {
		// 	notify.update('message', '<strong>Saving</strong> Page Data.');
		// }, 1000);
	}


	function showNotification(team, score) {
		color = 'success';

		$.notify(
			{
				// icon: 'nc-icon nc-trophy',
				icon: 'fa fa-bullseye',
				message: 'Ball in cup! Team <b>' + convertTeamToName(team) + '</b> reamining cups: ' + score
			},
			{
				type: color,
				timer: 5000,
				placement: {
					from: 'top',
					align: 'right'
				}
			}
		);
	}


	function populateScoreboard(){

		// LIVE SERVER
		// $.getJSON('../public-dashboard/assets/data/teams.json', function(data) {       
		$.getJSON('../assets/data/teams.json', function(data) {       
			console.log("Data...", data)  
			var team1 = data.team["1"]
			var team2 = data.team["2"]


			TEAM_HOME_NAME = team1.name;
			TEAM_AWAY_NAME = team2.name;
			HOME_CUPS = team1.numcups
			AWAY_CUPS = team2.numcups
			// team 1 => HOME
			$( "#home-team-name" ).html(team1.name);
			$( "#home-cups-left" ).html(team1.numcups);
			$( "#home-player-1" ).html(team1.player1);
			$( "#home-player-2" ).html(team1.player2);
			$( "#home-num-wins" ).html(team1.wins);
			$( "#home-num-losses" ).html(team1.losses);
			$( "#home-avg-score" ).html(team1.avgScore);
			$( "#home-image" ).attr("src", team1.avatar);

			

			// team 2 => AWAY
			$( "#away-team-name" ).html(team2.name);
			$( "#away-cups-left" ).html(team2.numcups);
			$( "#away-player-1" ).html(team2.player1);
			$( "#away-player-2" ).html(team2.player2);
			$( "#away-num-wins" ).html(team2.wins);
			$( "#away-num-losses" ).html(team2.losses);
			$( "#away-avg-score" ).html(team2.avgScore);
			$( "#away-image" ).attr("src", team2.avatar);
			


		});
	}

	function resetScoreboard(){
		$( "#home-team-name" ).html("N/A");
			$( "#home-cups-left" ).html("N/A");
			$( "#home-player-1" ).html("N/A");
			$( "#home-player-2" ).html("N/A");
			$( "#home-num-wins" ).html("N/A");
			$( "#home-num-losses" ).html("N/A");
			$( "#home-avg-score" ).html("N/A");
			$( "#home-image" ).attr("src", "https://via.placeholder.com/150?text=Team+1");

			

			// team 2 => AWAY
			$( "#away-team-name" ).html("N/A");
			$( "#away-cups-left" ).html("N/A");
			$( "#away-player-1" ).html("N/A");
			$( "#away-player-2" ).html("N/A");
			$( "#away-num-wins" ).html("N/A");
			$( "#away-num-losses" ).html("N/A");
			$( "#away-avg-score" ).html("N/A");
			$( "#away-image" ).attr("src", "https://via.placeholder.com/150?text=Team+2");
	}
	
	var resetBoard = document.getElementById('resetBoard');
	resetBoard.addEventListener('click', resetBoardF, false);
	function resetBoardF(){


		resetScoreboard();
		// clear timer 
		// https://stackoverflow.com/questions/8896327/jquery-wait-delay-1-second-without-executing-code
		setTimeout(function (){

			// Something you want delayed.
			populateScoreboard()
		}, 1000); 

		clearInterval(interval);
		startMatchIcon.getElementsByTagName( 'i' )[0].className = 'fa fa-play';
		secondsLabel.innerHTML = "00"
		minutesLabel.innerHTML = "00"

		sendEventToServer(
			JSON.stringify({ eventtype: RESET_BOARD,  deviceId: deviceID})
		);

		$( "#away-col" ).css("background-color", "");
		$( "#home-col" ).css("background-color", "");
	}


	function sendEventToServer(payload) {
		console.log('You called sendResetEventToServer()');
		
		console.log('SENDING DATA: ', payload);
		webSocket.send(payload);
	} 


	var startMatchIcon = document.getElementById('startMatch');
	startMatchIcon.addEventListener('click', startMatch, false);
	let interval;
	let matchPlaying = false;
	function startMatch() {
		if (matchPlaying) {
			console.log('stopping clock');
			clearInterval(interval);
			matchPlaying = false;
			startMatchIcon.getElementsByTagName( 'i' )[0].className = 'fa fa-play';
			sendEventToServer(
				JSON.stringify({ eventtype: STOP_BOARD,  deviceId: deviceID})
			);

		} else {
			console.log('Starting clock');
			interval = setInterval(setTime, 1000);
			matchPlaying = true;
			startMatchIcon.getElementsByTagName( 'i' )[0].className = 'fa fa-pause';
			// sendEventToServer(START_BOARD);	
			sendEventToServer(
				JSON.stringify({ 
					eventtype: START_BOARD,  
					deviceId: deviceID, 
					homecups: HOME_CUPS,
					awaycups: AWAY_CUPS, 
					method: OPEN_CV})
			);		
			
		}
	}

	var minutesLabel = document.getElementById('timer-minutes');
	var secondsLabel = document.getElementById('timer-seconds');
	var totalSeconds = 0;
	function setTime() {
		++totalSeconds;
		secondsLabel.innerHTML = pad(totalSeconds % 60);
		minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
	}
	function pad(val) {
		var valString = val + '';
		if (valString.length < 2) {
			return '0' + valString;
		} else {
			return valString;
		}
	}

	function convertTeamToName(team){
		if (team == TEAM_HOME){
			return TEAM_HOME_NAME;
		}else if (team == TEAM_AWAY){
			return TEAM_AWAY_NAME;
		} else return "NO TEAM GIVEN!"
	}

	////////////////////// FAKE LEADERBOARD //////////////////////////////
	// https://codepen.io/nsa94/pen/wmYgLY
	// var userids =
	// 	'3125964;7469625;8537370;8525793;8550389;8537351;7429009;8540694;8529267;8538329;8030256;8538080;8535715;8559510;8538112;8522223;8709661;7992142';
	// var num = userids.split(';').length;
	// var url = 'https://api.stackexchange.com/2.2/users/' + userids + '?order=desc&sort=reputation&site=stackoverflow';
	// $.getJSON(url, function(data) {
	// 	for (var i = 0; i < num; i++) {
	// 		$('#leaderboard tbody').append(
	// 			'<tr> <td>' +
	// 				(i + 1) +
	// 				"</td><td><img class='avatar' src='" +
	// 				data.items[i].profile_image +
	// 				"'/>" +
	// 				data.items[i].display_name +
	// 				"</td><td class='text-right'>" +
	// 				data.items[i].reputation +
	// 				'</td></tr>'
	// 		);
	// 	}
	// });
});
