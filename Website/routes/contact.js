var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('contact', { title: 'SportsCanary - Predicting the future of Sports with Big Data.' });
});

module.exports = router;