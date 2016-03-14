var express = require('express'),
    router = express.Router(),
    //url = require('url'),
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

/* GET games page. */
router.route('/games')

    .get(function(req, res, next) {
        var query = require('url').parse(req.url,true).query;
        if(query.date == "" || query.date == undefined) {
            mongoose.model('MM_Game').find({}, function (err, results) {
                if (err) {
                    return console.error(err);
                } else {
                    res.format({
                        json: function () {
                            res.json(results);
                        }
                    });
                }
            });
        } else {
            var tomorrows_date = new Date();
            tomorrows_date.setDate(tomorrows_date.getDate() + 1);
            tomorrows_date = tomorrows_date.toLocaleDateString();
            mongoose.model('MM_Game').find({"date": {"$gte": new Date().toLocaleDateString(), "$lt": tomorrows_date}},
                function (err, results) {
                if (err) {
                    return console.error(err);
                } else {
                    res.format({
                        json: function () {
                            res.json(results);
                        }
                    });
                }
            });
        }
    });

module.exports = router;