var express = require('express'),
    router = express.Router(),
    // MongoDB Connection
    mongoose = require('mongoose'),
    result = mongoose.model('Result'),
    // Parses Body
    bodyParser = require('body-parser'),
    // Manipulates Post
    methodOverride = require('method-override');

router.use(bodyParser.urlencoded({ extended: true }));
router.use(methodOverride(function(req, res){
    if (req.body && typeof req.body === 'object' && '_method' in req.body) {
        // look in urlencoded POST bodies and delete it
        var method = req.body._method;
        delete req.body._method;
        return method
    }
}));

router.route('/')
    .get(function(req, res, next) {
        mongoose.model('Result').find({}, function (err, results) {
            if (err) {
                return console.error(err);
            } else {
                res.format({
                    html: function(){
                        res.render('results/index', {
                            title: 'All my Results',
                            "results" : results
                        });
                    },
                    json: function(){
                        res.json(results);
                    }
                });
            }
        });
    })
    .post(function(req, res) {
        var event_name = req.body.event_name;
        var score_applicable = req.body.score_applicable;
        var score_1 = req.body.score_1;
        var score_2 = req.body.score_2;
        var event_date = req.body.event_date;
        mongoose.model('Result').create({
            event_name : event_name,
            score_applicable : score_applicable,
            score_1 : score_1,
            score_2 : score_2,
            event_date : event_date
        }, function (err, result) {
            if (err) {
                res.send("There was a problem adding the information to the database.");
            } else {
                console.log('POST new result: ' + result);
                res.format({
                    html: function(){
                        res.location("/api/results");
                        res.redirect("/api/results");
                    },
                    json: function(){
                        res.json(result);
                    }
                });
            }
        })
    });
router.get('/new', function(req, res) {
    res.render('results/new', { title: 'Add New Result' });
});
router.param('id', function(req, res, next, id) {
    console.log('Validating ' + id + ' exists.');
    mongoose.model('Result').findById(id, function (err, result) {
        if (err) {
            console.log(id + ' was not found');
            res.status(404);
            var err = new Error('Not Found');
            err.status = 404;
            res.format({
                html: function(){
                    next(err);
                },
                json: function(){
                    res.json({message : err.status  + ' ' + err});
                }
            });
            //if it is found we continue on
        } else {
            req.id = id;
            next();
        }
    });
});
router.route('/:id')
    .get(function(req, res) {
        mongoose.model('Result').findById(req.id, function (err, result) {
            if (err) {
                console.log('GET Error: There was a problem retrieving: ' + err);
            } else {
                //console.log('GET Retrieving ID: ' + result.event_name);
                res.format({
                    html: function(){
                        res.render('results/show', {
                            "result" : result
                        });
                    },
                    json: function(){
                        res.json(result);
                    }
                });
            }
        });
    });
router.get('/:id/edit', function(req, res) {
    mongoose.model('Result').findById(req.id, function (err, result) {
        if (err) {
            console.log('GET Error: There was a problem retrieving: ' + err);
        } else {
            console.log('GET Retrieving ID: ' + result._id);
            //format the date properly for the value to show correctly in our edit form
            res.format({
                html: function(){
                    res.render('results/edit', {
                        title: 'Result ' + result._id,
                        "result" : result
                    });
                },
                json: function(){
                    res.json(result);
                }
            });
        }
    });
});
router.put('/:id/edit', function(req, res) {
    var event_name = req.body.event_name;
    var score_applicable = req.body.score_applicable;
    var score_1 = req.body.score_1;
    var score_2 = req.body.score_2;
    var event_date = req.body.event_date;

    //find the document by ID
    mongoose.model('Result').findById(req.id, function (err, result) {
        //update it
        result.update({
            event_name : event_name,
            score_applicable : score_applicable,
            score_1 : score_1,
            score_2 : score_2,
            event_date : event_date
        }, function (err, resultID) {
            if (err) {
                res.send("There was a problem updating the information to the database: " + err);
            }
            else {
                res.format({
                    html: function(){
                        res.redirect("/api/results/" + result._id);
                    },
                    json: function(){
                        res.json(result);
                    }
                });
            }
        })
    });
});
router.delete('/:id/edit', function (req, res){
    mongoose.model('Result').findById(req.id, function (err, result) {
        if (err) {
            return console.error(err);
        } else {
            result.remove(function (err, result) {
                if (err) {
                    return console.error(err);
                } else {
                    console.log('DELETE removing ID: ' + result._id);
                    res.format({
                        html: function(){
                            res.redirect("/api/results");
                        },
                        json: function(){
                            res.json({message : 'deleted',
                                item : result
                            });
                        }
                    });
                }
            });
        }
    });
});
module.exports = router;