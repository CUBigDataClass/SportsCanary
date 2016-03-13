var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('Index', function() {
    it('Should return our search file', function(done) {
        chai.request(server)
            .get('/search')
            .end(function(err, res) {
                res.should.have.status(200);
                done();
            });
    });
    it('Should return a json file with our searches', function(done) {
        chai.request(server)
            .get('/search?category=vs')
            .end(function(err, res) {
                res.should.have.status(200);
                res.should.be.json;
                done();
            });
    });
});