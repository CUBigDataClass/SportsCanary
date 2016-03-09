var mongoose = require('mongoose');
var resultSchema = new mongoose.Schema({
    event_name: String,
    score_applicable: Boolean,
    score_1: Number,
    score_2: Number,
    event_date: { type: Date, default: Date.now }
});
mongoose.model('Result', resultSchema);