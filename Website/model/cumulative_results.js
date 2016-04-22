var mongoose = require('mongoose');

var cumulativeResultSchema = new mongoose.Schema({
    sport_type: String,
    predicted_percent: Number,
    game_count: Number,
    tweet_count: Number
});
mongoose.model('CumulativeResult', cumulativeResultSchema);