var express = require('express'),
    router = express.Router(),
    mongoose = require('mongoose'),
    result = mongoose.model('Result');

router.route('/').get(function(req, res, next) {
    mongoose.model('Result').find({}, function (err, results) {
        if (err) {
            return console.error(err);
        } else {
            res.format({
                html: function() {
                    results = results.reverse();
                    res.render('sports/results-index', {
                        title: 'SportsCanary - Predictions for Basketball, Baseball and Hockey',
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
                        title: 'SportsCanary - Predictions: NBA',
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
                        title: 'SportsCanary - Predictions: NHL',
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
                        title: 'SportsCanary - Predictions: MLB',
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
router.route('/kobe').get(function(req, res, next) {
    mongoose.model('Result').find({'sport_type': 'mlb'}, function (err, results_kobe) {
        if (err) {
            return console.error(err);
        } else {
            res.format({
                html: function(){
                    res.render('sports/kobe', {
                        title: 'SportsCanary - Kobe: Mamba Day',
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