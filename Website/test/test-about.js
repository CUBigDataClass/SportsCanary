var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('about', function() {
	it('Should return about page.', function(done) {
		chai.request(server)
		.get('/about')
		.end(function(err, res) {
			res.should.have.status(200);
			res.should.be.html;
			
			done();
		});
	});
});