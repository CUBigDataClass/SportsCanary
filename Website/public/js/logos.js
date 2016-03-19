function getLogoForTeam(team) {
    switch(team) {
    case '321':
    case 1:
       alert('Hey');
       break;
    default:
    	console.log("Error");
        return "images/nba_logos/Error-img.jpeg";
		break;
	}           
}