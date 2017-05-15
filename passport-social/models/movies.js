var mongoose = require('mongoose');

var movieSchema = mongoose.Schema({
    user_id : Number,
    movie_id : Number,
    rating : Number
});

// create the model for users and expose it to our app
module.exports = mongoose.model('Movie', movieSchema);