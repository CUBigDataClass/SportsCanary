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
                        title: 'SportsCanary - Predictions for Basketball, Hockey',
                        "results" : results
                    });
                }
            });
        }
    });
});
module.exports = router;