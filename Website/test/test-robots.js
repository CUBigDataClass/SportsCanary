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
		// TODO - Write tests to check that robots.txt have the correct body.
		.end(function(err, res) {
			res.should.have.status(200);
			chai.expect(res.should.be.text);
			done();
		});
	});
});