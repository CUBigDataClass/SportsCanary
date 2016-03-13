var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('search/search', { title: 'SportsCanary - Search' });
});

module.exports = router;