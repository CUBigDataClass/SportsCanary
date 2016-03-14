var mongoose = require('mongoose');

var mm_gameSchema = new mongoose.Schema({
    date: Date,
    label: String,
    data_team_1: {
        home_or_away: String,
        seed: Number,
        team_id: String,
        score: Number
    },
    data_team_2: {
        home_or_away: String,
        seed: Number,
        team_id: String,
        score: Number
    }
});
mongoose.model('MM_Game', mm_gameSchema);