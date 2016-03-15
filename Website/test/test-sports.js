var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('sports', function() {
	it('Should return about page.', function(done) {
		chai.request(server)
		.get('/sports')
		.end(function(err, res) {
			res.should.have.status(200);
			res.should.be.html;
			
			done();
		});
	});
});