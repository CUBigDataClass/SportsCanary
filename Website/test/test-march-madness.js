var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('Results', function() {
    var id = 0;
    it('should list ALL teams on /api/march_madness/teams GET', function(done) {
        chai.request(server)
            .get('/api/march_madness/teams')
            .end(function(err, res){
                res.should.have.status(200);
                chai.expect(res.should.be.json);
                done();
            });
    });
    it('should list ALL games on /api/march_madness/games GET', function(done) {
        chai.request(server)
            .get('/api/march_madness/games')
            .end(function(err, res){
                res.should.have.status(200);
                chai.expect(res.should.be.json);
                done();
            });
    });
    it('should list ALL games for today on /api/march_madness/games?date=today GET', function(done) {
        chai.request(server)
            .get('/api/march_madness/games?date=today')
            .end(function(err, res){
                res.should.have.status(200);
                chai.expect(res.should.be.json);
                done();
            });
    });
});