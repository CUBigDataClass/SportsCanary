var mongoose = require('mongoose');

var mm_teamSchema = new mongoose.Schema({
    seed: Number,
    team: String,
    college: String,
    conference: String
});
mongoose.model('MM_Team', mm_teamSchema);