var express = require('express'),
    router = express.Router(),
    mongoose = require('mongoose'),
    result = mongoose.model('Result');

router.route('/')
.get(function(req, res, next) {
    mongoose.model('Result').find({}, function (err, results) {
        if (err) {
            return console.error(err);
        } else {
            res.format({
                html: function() {
                    res.render('sports/results-index', {
                        title: 'SportsCanary - Predictions for Basketball, Hockey and Basketball',
                        "results" : results
                    });
                }
            });
        }
    });
});
router.route('/nba').get(function(req, res, next) {
    mongoose.model('Result').find({'sport_type': 'nba'}, function (err, results_nba) {
        if (err) {
            return console.error(err);
        } else {
            res.format({
                html: function(){
                    results_nba = results_nba.reverse();
                    res.render('sports/results-nba', {
                        title: 'Results',
                        "results_nba" : results_nba
                    });
                },
                json: function(){
                    res.json(results_nba);
                }
            });
        }
    });
});
router.route('/nhl').get(function(req, res, next) {
    mongoose.model('Result').find({'sport_type': 'nhl'}, function (err, results_nhl) {
        if (err) {
            return console.error(err);
        } else {
            res.format({
                html: function(){
                    results_nhl = results_nhl.reverse();
                    res.render('sports/results-nhl', {
                        title: 'Results',
                        "results_nhl" : results_nhl
                    });
                },
                json: function(){
                    res.json(results_nhl);
                }
            });
        }
    });
});
router.route('/mlb').get(function(req, res, next) {
    mongoose.model('Result').find({'sport_type': 'mlb'}, function (err, results_mlb) {
        if (err) {
            return console.error(err);
        } else {
            res.format({
                html: function(){
                    results_mlb = results_mlb.reverse();
                    res.render('sports/results-mlb', {
                        title: 'Results',
                        "results_mlb" : results_mlb
                    });
                },
                json: function(){
                    res.json(results_mlb);
                }
            });
        }
    });
});
module.exports = router;