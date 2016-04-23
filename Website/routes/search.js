var express = require('express');
var url = require('url');
var mongoose = require('mongoose');
var router = express.Router();
var elasticsearch = require('elasticsearch');
var result = mongoose.model('Result');

router.get('/', function(req, res, next) {
    var url_parts = url.parse(req.url, true);
    var query = url_parts.query;
    var category = query.category;

    if(category === "" || category === null) {
        res.render('search/search', { title: 'SportsCanary - Search'});
    } else {
        //var client = new elasticsearch.Client({
        //    host: 'localhost:9200',
        //    // Change to trace in development
        //    log: 'info'
        //});
        result.find({ $or: [{'team_1_name': category}, {'team_2_name': category}, {'event_name': category}]}, function (err, results) {
            if (err) {
                return console.error(err);
            } else {
                if (results.length == 0) {
                    res.render('search/search', {title: 'SportsCanary - Search'});
                } else {
                    res.format({
                        html: function () {
                            results = results.reverse();
                            res.render('sports/results-index', {
                                title: 'SportsCanary - Predictions for Basketball, Hockey and Basketball',
                                "results": results
                            });
                        },
                        json: function () {
                            res.json(results);
                        }
                    });
                }
            }
        });
        //client.search({
        //    index: 'sportscanary',
        //    body: {
        //        query: {
        //            match: {
        //                _all: cat
        //            }
        //        }
        //    }
        //}).then(function (resp) {
        //    var hits = resp.hits.hits;
        //    res.json(hits);
        //}, function (err) {
        //    console.trace(err.message);
        //    res.render('search/search', { title: 'SportsCanary - Search'});
        //});
    }
});

module.exports = router;