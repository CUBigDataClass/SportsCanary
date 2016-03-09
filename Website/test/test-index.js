var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('Index', function() {
  it('Should return our index file', function(done) {
  	chai.request(server)
  		.get('/')
  		.end(function(err, res) {
  			res.should.have.status(200);
  			done();
  		});
  });
});