var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('contacts', function() {
	it('should return contacts page.', function(done) {
		chai.request(server)
		.get('/contacts/index.html')
		//Add 
		.end(function(err, res) {
			res.should.have.status(200);
			res.should.be.text;
			done();
		});
	});
});