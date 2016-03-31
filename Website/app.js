var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var db = require('./model/db');
var result = require('./model/results');
var mm_team = require('./model/mm_teams');
var mm_game = require('./model/mm_games');
var robots = require('robots.txt');
var routes = require('./routes/index');
var results = require('./routes/results');
var search = require('./routes/search');
var sports = require('./routes/sports');
var march_madness = require('./routes/march_madness');
var about = require('./routes/about');
var contact = require('./routes/contact');
var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/components', express.static(__dirname + '/bower_components'));

// Pass in the absolute path to your robots.txt file
app.use(robots(__dirname + '/robots.txt'));
app.use('/', routes);
app.use('/api/results', results);
app.use('/search', search);
app.use('/sports', sports);
app.use('/api/march_madness', march_madness);
app.use('/about', about);
app.use('/contact', contact);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('404: Not Found :(');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
//if (app.get('env') === 'development') {
//  app.use(function(err, req, res, next) {
//    res.status(err.status || 500);
//    res.render('error', {
//      message: err.message,
//      error: err
//    });
//  });
//}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});


module.exports = app;
