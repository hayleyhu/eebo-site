$(function(){
	$("#submit").click(function(){
		console.log('I got here');
		$("#groupheader").css("background-color","red");
	});
	var hashValue = window.location.hash.substr(1);
	if (hashValue == "app") {
		$("#matchtable > tbody:last").append('<tr><td>4</td><td>18:00-18:30</td><td>Dan</td><td>224-1114444</td><td>dandan2018@u.northwestern.edu</td></tr>'); }
});
