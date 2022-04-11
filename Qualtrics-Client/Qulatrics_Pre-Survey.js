Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/
	const maxTimeAllowed = 40 //in seconds
	var timeFromServer = 0;
	var qobj = this;
	qobj.hideNextButton();
	console.log("trying to connect now")
	const socket = io.connect('http://127.0.0.1:5000');
	console.log("Connected")

	socket.on('connect', function() {
		socket.send('User has connected')
	})

	var reponseServer = "";
	console.log("Start receiving now")
	socket.on('message', function(msg) {
		 console.log('Received message' + msg);
		if (msg === "Continue"){
			reponseServer = msg;
			qobj.showNextButton();
			console.log("this is working");
			qobj.clickNextButton();
		}
		else{
			timeFromServer = parseInt(msg);
			console.log(timeFromServer);
		}
	});

	setTimeout(function(){
		var ts = Math.round((new Date()).getTime() / 1000);
		console.log("Current time stamps is "+ts);
		var timeForWait = timeFromServer+maxTimeAllowed - ts;
		console.log("time for wait is "+timeForWait);
		if(timeForWait > 0){
			timeForWait = timeForWait*1000;
		}
		else{
			timeForWait = 0;
		}

		setTimeout(function() {
			qobj.showNextButton();
			qobj.clickNextButton();
		}, timeForWait);
	},10000);


});