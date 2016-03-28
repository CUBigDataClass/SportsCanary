var express = require('express');
var url = require('url');
var router = express.Router();
var elasticsearch = require('elasticsearch');
router.get('/', function(req, res, next) {
    var url_parts = url.parse(req.url, true);
    var query = url_parts.query;
    var cat = query.category;


    if(cat === "" || cat === null) {
        res.render('search/search', { title: 'SportsCanary - Search'});
    } else {
        var client = new elasticsearch.Client({
            host: 'localhost:9200',
            // Change to trace in development
            log: 'info'
        });

        client.search({
            index: 'sportscanary',
            body: {
                query: {
                    match: {
                        _all: cat
                    }
                }
            }
        }).then(function (resp) {
            var hits = resp.hits.hits;
            res.json(hits);
        }, function (err) {
            console.trace(err.message);
            res.render('search/search', { title: 'SportsCanary - Search'});
        });
    }
});

module.exports = router;