var chai = require('chai');
var chaiHttp = require('chai-http');
var server = require('../app');
var should = chai.should();

chai.use(chaiHttp);


describe('Results', function() {
    var id = 0;
    it('should list ALL results on /api/results GET', function(done) {
        chai.request(server)
            .get('/api/results')
            .end(function(err, res){
                res.should.have.status(200);
                res.should.be.html;
                done();
            });
    });
    it('should add a SINGLE result on /api/results POST', function(done) {
        chai.request(server)
            .post('/api/results')
            .send({'event_name': 'Test Game', 'score_applicable': true,
                    'score_1': 123, 'score_2': 321, 'event_date': Date.now()})

            .end(function(err, res){
                res.should.have.status(200);
                res.should.be.json;
                res.body.should.be.a('object');
                res.body.should.have.property('__v');
                res.body.should.have.property('event_name');
                res.body.should.have.property('score_1');
                res.body.should.have.property('score_2');
                res.body.should.have.property('_id');
                id = res.body['_id'];
                res.body.should.have.property('event_date');
                res.body.event_name.should.equal('Test Game');
                done();
            });
    });
    it('should list a SINGLE blob on /blob/<id> GET', function(done) {
        chai.request(server)
            .get('/api/results/' + id)
            .send({'event_name': 'Test Game', 'score_applicable': true,
                'score_1': 123, 'score_2': 321, 'event_date': Date.now()})

            .end(function(err, res){
                res.should.have.status(200);
                res.should.be.json;
                res.body.should.be.a('object');
                res.body.should.have.property('__v');
                res.body.should.have.property('event_name');
                res.body.should.have.property('score_1');
                res.body.should.have.property('score_2');
                res.body.should.have.property('_id');
                res.body.should.have.property('event_date');
                res.body.event_name.should.equal('Test Game');
                done();
            });
    });
    it('should update a SINGLE blob on /blob/<id> PUT');
    it('should delete a SINGLE blob on /blob/<id> DELETE');
});