var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();
request = require("request");

chai.use(chaiHttp);


describe('Robots', function() {
	it('should return robots.txt file in text/plain format.', function(done) {
		chai.request(server)
		.get('/robots.txt')
		.end(function(err, res) {
			res.should.have.status(200);
			res.should.be.text;
			done();
		});
	});
	it('should return robots.txt file in text/plain format.', function(done) {
		chai.request(server)
		.get('/robots.txt')
		.end(function(err, res) {
			res.should.have.status(200);
			// TODO - Write tests to check that robots.txt have the correct body.
			done();
		});
	});
});