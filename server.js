/**
 * Module dependencies.
 */
var express = require('express');
var session = require('client-sessions');
var favicon = require('serve-favicon');
var path = require('path');
var PythonShell = require('python-shell');
var connection = require('express-myconnection');
var mysql = require('mysql');


//var routes = require('./routes');
var http = require('http');

//load customers route
//var customers = require('./routes/customers'); 
var app = express();

// all environments
app.set('port', process.env.PORT || 8080);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
//app.use(favicon(__dirname + '/public/favicon.ico'));
//app.use(express.logger('dev'));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/suggestions', function(req,res){
  var options = {
	  scriptPath: './algorithms',
	  args: ['usercf', '1', '10']
	};
	PythonShell.run('recommendations.py', options, function (err, results) {
	  if (err) throw err;
	  // results is an array consisting of messages collected during execution
	  
	  res.json(JSON.parse(results));
	});
});

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});