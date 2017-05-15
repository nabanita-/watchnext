var fs = require('fs'),
    readline = require('readline'),
    User = require("./models/user");
var dbConfig = require('./config/db');
var mongoose = require('mongoose');
mongoose.connect(dbConfig.url);

var rd = readline.createInterface({
    input: fs.createReadStream('../algorithms/ml-100k/u.user'),
    output: process.stdout,
    terminal: false
});

rd.on('line', function(line) {
    var arr=line.toString().split('|');
    console.log(arr[0]);
    var newUser = new User();
    newUser.personal.id=arr[0];
    newUser.personal.email="user"+arr[0]+"@mymoviez.com";
    newUser.personal.gender=arr[2];
    newUser.personal.occupation=arr[3];
    newUser.personal.password=newUser.generateHash("12345");
    newUser.personal.state=arr[4];
    newUser.save(function(err,data) {
                    if (err)
                        throw err;
                    console.log(data._id);
                    //return done(null, newUser);
                });
});