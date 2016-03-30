require('dotenv').config({path: 'env.env'});
var aws_user = process.env['AWS_MONGO_USER'];
var aws_pass = process.env['AWS_MONGO_PASS'];
var aws_address = process.env['AWS_ADDRESS'];

var mongoose = require('mongoose');

console.log('mongodb://' + aws_user + ':' + aws_pass + '@' + aws_address);
mongoose.connect('mongodb://' + aws_user + ':' + aws_pass + '@' + aws_address);