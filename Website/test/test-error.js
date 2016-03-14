var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('Index', function() {
    it('Should return a 404', function(done) {
        chai.request(server)
            .get('/not_a_real_endpoint')
            .end(function(err, res) {
                res.should.have.status(404);
                done();
            });
    });
});