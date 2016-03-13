var express = require('express');
var router = express.Router();
var elasticsearch = require('elasticsearch');
/* GET home page. */
router.get('/', function(req, res, next) {

    var client = new elasticsearch.Client({
        host: 'localhost:9200',
        // Change to info in development
        log: 'trace'
    });

    client.search({
        index: 'sportscanary',
        body: {
            query: {
                match: {
                    _all: 'vs'
                }
            }
        }
    }).then(function (resp) {
        var hits = resp.hits.hits;
        console.log(hits);
        res.json(hits)
    }, function (err) {
        console.trace(err.message);
    });

    //res.render('search/search', { title: 'SportsCanary - Search', games: hits });
});

module.exports = router;