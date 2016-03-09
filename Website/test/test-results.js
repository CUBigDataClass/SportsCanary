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
    it('should list a SINGLE result on /api/results/<id> GET', function(done) {
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
    // TODO - Handle not sending every parameter in PUT
    it('should update a SINGLE result on /api/results/<id>/edit PUT', function(done) {
        chai.request(server)
            .put('/api/results/' + id + '/edit')
            .send({'event_name': 'New Name', 'score_applicable': true, 'score_1': 10, 'score_2': 90, event_date: Date.now()})
            .end(function (error, response) {
                response.should.have.status(200);
                response.should.be.json;
                response.body.should.be.a('object');
                response.body.should.have.property('ok', 1);
                done();
            });
    });
    it('should delete a SINGLE result on /api/results/<id>/edit DELETE', function(done) {
        chai.request(server)
            .delete('/api/results/' + id + '/edit')
            .end(function (error, response) {
                response.should.have.status(200);
                response.should.be.json;
                response.body.should.be.a('object');
                response.body.should.have.property('message', 'deleted');
                response.body.should.have.property('item');
                response.body.item.should.be.a('object');
                response.body.item.should.have.property('__v');
                response.body.item.should.have.property('event_name');
                response.body.item.should.have.property('score_1');
                response.body.item.should.have.property('score_2');
                response.body.item.should.have.property('_id');
                response.body.item.should.have.property('event_date');
                done();
        });
    });
});