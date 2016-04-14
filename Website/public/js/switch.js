function switch_team(team_logo) {

  var team_logo = 'atlanta-hawks';
  var photo_src = 'images/nba_logos/';
  switch (team_logo) {
    case "atlanta-hawks":
      photo_src += 'atlanta-hawks' + '.png';
      console.log(photo_src);
      break;
    case "milwaukee-bucks":
      console.log("Hello 👍milwaukee-bucks");
      break;
    case "boston-celtics":
      console.log("boston-celtics.");
      break;
    case "minnesota-timberwolves":
      console.log("minnesota-timberwolves.");
      break;
    case "brooklyn-nets":
      console.log("brooklyn-nets");
      break;
    case "new-orleans-hornets":
      console.log("switch called");
      break;
    case "charlotte-bobcats":
      console.log("switch called");
      break;
    case "new-york-knicks":
      console.log("switch called");
      break;
    case "chicago-bulls":
      console.log("switch called");
      break;
    case "oklahoma-city-thunder":
      console.log("switch called");
      break;
    case "cleveland-cavaliers":
      console.log("switch called");
      break;
    case "orlando-magic":
      console.log("switch called");
      break;
    case "dallas-mavericks":
      console.log("switch called");
      break;
    case "philadelphia-76ers":
      console.log("switch called");
      break;
    case "denver-nuggets":
      console.log("switch called");
      break;
    case "phoenix-suns":
      console.log("switch called");
      break;
    case "detroit-pistons":
      console.log("switch called");
      break;
    case "portland-trail-blazers":
      console.log("switch called");
      break;
    case "golden-state-warriors":
      console.log("switch called");
      break;
    case "sacramento-kings":
      console.log("switch called");
      break;
    case "houston-rockets":
      console.log("switch called");
      break;
    case "san-antonio-spurs":
      console.log("switch called");
      break;
    case "indiana-pacers":
      console.log("switch called");
      break;
    case "toronto-raptors":
      console.log("switch called");
      break;
    case "los-angeles-clippers":
      console.log("switch called");
      break;
    case "utah-jazz":
      console.log("switch called");
      break;
    case "los-angeles-lakers":
      console.log("switch called");
      break;
    case "memphis-grizzlies":
      console.log("switch called");
      break;
    case "washington-wizards":
      console.log("switch called");
      break;
    case "miami-heat":
      console.log("switch called");
      break;
    case "test":
      console.log("switch called");
      break;

    default:
      console.log("in switch team_logo: " + team_logo + " was Not Found.");
  }
}
