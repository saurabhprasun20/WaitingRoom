Qualtrics.SurveyEngine.addOnPageSubmit(function()
{
	console.log("url_choice is:"+url_choice);
	console.log("embedded flag is:"+ flag_embeded);
	var workerid = Qualtrics.SurveyEngine.getEmbeddedData("workerId");
	var assignmentId = Qualtrics.SurveyEngine.getEmbeddedData("assignmentId");
	var hitId = Qualtrics.SurveyEngine.getEmbeddedData("hitId");
	console.log(workerid);
	var worker_param = "?mTurkId="+workerid
	var assignment_param = "&assignmentId="+assignmentId
	var hit_param = "&hitId="+hitId
	
	/*Place your JavaScript here to run when the page loads*/
	const chat_version = ["https://discussionroom.org/KkhDj%2Bm3qFXhaYVeG076c%2BkMkE24kW1Sjinni8q9lr4%3D/"+worker_param+assignment_param+hit_param, 
						  "https://discussionroom.org/KkhDj%2Bm3qFXhaYVeG076c%2BkMkE24kW1Sjinni8q9lr4%3D/"+worker_param+assignment_param+hit_param, 
						  "https://discussionroom.org/KkhDj%2Bm3qFXhaYVeG076c%2BkMkE24kW1Sjinni8q9lr4%3D/"+worker_param+assignment_param+hit_param,
						  "https://discussionroom.org/KkhDj%2Bm3qFXhaYVeG076c%2BkMkE24kW1Sjinni8q9lr4%3D/"+worker_param+assignment_param+hit_param
						 ];
	console.log("this");
	console.log(chat_version[url_choice]);
	setTimeout(function () {
	window.location.href = chat_version[url_choice];},5000)

	
	
	/*nb = document.querySelector("#NextButton")
	nb.onclick = setTimeout(function () {
		window.location.href = chat_version[url_choice];},15000)*/
});

Qualtrics.SurveyEngine.addOnReady(function()
{
	/*Place your JavaScript here to run when the page is fully displayed*/

});

Qualtrics.SurveyEngine.addOnUnload(function()
{
	/*Place your JavaScript here to run when the page is unloaded*/

});