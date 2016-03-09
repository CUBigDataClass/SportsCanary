var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'SportsCanary - Predicting the future with Big Data.' });
});

module.exports = router;
