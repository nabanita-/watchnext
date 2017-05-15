var mongoose = require('mongoose');
var bcrypt   = require('bcrypt-nodejs');


var userSchema = mongoose.Schema({
    personal:{
    	id : Number,
		email: String,
		phone : String,
		name : String,
		gender : String,
		occupation : String,
		password : String,
		state : String
	},
	fb: {
		id: String,
		access_token: String,
		firstName: String,
		lastName: String,
		email: String
	},
	twitter: {
		id: String,
		token: String,
		username: String,
		displayName: String,
		lastStatus: String
	},
     google: {
        id : String,
        token : String,
        email : String,
        name : String
    }	
});
userSchema.methods.generateHash = function(password) {
    return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

// checking if password is valid
userSchema.methods.validPassword = function(password) {
    return bcrypt.compareSync(password, this.personal.password);
};

// create the model for users and expose it to our app
module.exports = mongoose.model('User', userSchema);