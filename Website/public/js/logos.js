
function getlogo(team) {
    switch(team) {
    case '321':
    case 'larry': 
       alert('Hey');
       break;
    default:
    	console.log("Error");
        return "images/nba_logos/Error-img.jpeg";
		break;
	}           
}