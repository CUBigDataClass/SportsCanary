var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var result = mongoose.model('Result');

/* GET home page. */
router.get('/', function(req, res, next) {
  mongoose.model('Result').find({'sport_type': 'mlb'}, function (err, mlb_results) {
    if (err) {
      return console.error(err);
    } else {
      mongoose.model('Result').find({'sport_type': 'nba'}, function (err, nba_results) {
        if (err) {
          return console.error(err);
        } else {
          mongoose.model('Result').find({'sport_type': 'nhl'}, function (err, nhl_results) {
            if (err) {
              return console.error(err);
            } else {
              res.format({
                html: function () {
                  res.render('index', {
                    title: 'SportsCanary - Predicting the future of Sports with Big Data.',
                    "mlb_results": mlb_results,
                    "nba_results": nba_results,
                    "nhl_results": nhl_results
                  });
                }
              });
            }
          }).limit(1).sort({'event_date': -1});
        }
      }).limit(1).sort({'event_date': -1});
    }
  }).limit(1).sort({'event_date': -1});
});

module.exports = router;