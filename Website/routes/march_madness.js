var express = require('express'),
    router = express.Router(),
// MongoDB Connection
    mongoose = require('mongoose'),
    team = mongoose.model('MM_Team'),
// Parses Body
    bodyParser = require('body-parser'),
    crypto = require('crypto'),
    assert = require('assert'),
// Manipulates Post
    methodOverride = require('method-override');



router.get('/', function(req, res, next) {
    res.render('index', { title: 'Teams Index' });
});

/* GET teams page. */
router.route('/teams')
    .get(function(req, res, next) {
        mongoose.model('MM_Team').find({}, function (err, results) {
            if (err) {
                return console.error(err);
            } else {
                res.format({
                    json: function(){
                        res.json(results);
                    }
                });
            }
        });
    });

module.exports = router;