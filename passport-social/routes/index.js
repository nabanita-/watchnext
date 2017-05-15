var express = require('express');
var PythonShell = require('python-shell');
var request = require('request');
var fs = require("fs");
var Movie = require('../models/movies');

var router = express.Router();

var isAuthenticated = function (req, res, next) {
	// if user is authenticated in the session, call the next() to call the next request handler 
	// Passport adds this method to request object. A middleware is allowed to add properties to
	// request and response objects
	if (req.isAuthenticated())
		return next();
	// if the user is not authenticated then redirect him to the login page
	res.redirect('/login');
}

module.exports = function(passport){

	/* GET login page. */
	router.get('/', function(req, res) {
    	// Display the Login page with any flash message, if any
		res.render('landing', {message: req.flash('message') });
	});
	router.get('/login', function(req, res) {
    	// Display the Login page with any flash message, if any
		res.render('login', { message: req.flash('message') });
	});

	/* Handle Login POST */
	router.post('/login', passport.authenticate('login', {
		successRedirect: '/home',
		failureRedirect: '/',
		failureFlash : true  
	}));

	/* GET Registration Page */
	router.get('/signup', function(req, res){
		res.render('userRegister',{message: req.flash('message')});
	});

	/* Handle Registration POST */
	router.post('/signup', passport.authenticate('signup', {
		successRedirect: '/home',
		failureRedirect: '/signup',
		failureFlash : true  
	}));

	/* GET Home Page */
	router.get('/watchnext',isAuthenticated, function(req, res){
		var u = req.user.personal.id;
		var options1 = {
			scriptPath: '../../algorithms',
			args: ['usercf', u, '15']
		};	
		var options2 = {
			scriptPath: '../../algorithms',
			args: ['itemcf', u, '15']
		};
		PythonShell.run('recommendations.py', options1, function (err1, usercf) {
			if (err1) throw err1;
	  	PythonShell.run('recommendations.py',options2,function(err2, itemcf) {
	  	    if (err2) throw err2;
      		res.render('myrecs',{'movies': JSON.parse(usercf),'movies1':JSON.parse(itemcf),'user' : req.user.personal.id});
	  	});
		});
		var u = req.user.personal.id;
		});

	router.get('/bsproject',isAuthenticated, function(req, res){
		var u = req.user.personal.id;
		var options = {
		  scriptPath: '../../algorithms',
		  args: [u]
		};
		PythonShell.run('myratings.py',options,function(err2, rmovies) {
		  	    if (err2) throw err2;
		  	    if (rmovies==null){
		  	    	var options1 = {
						scriptPath: '../../algorithms',
						args: ['25']
					};
		  			PythonShell.run('wilson.py',options,function(err2, wilsonrated) {
		  	    		if (err2) throw err2;
		  	    		res.render('norating',{'movies':JSON.parse(wilsonrated),'user' : req.user.personal.id});
		  			});
		  	    }
		  	    else{
					var options1 = {
						scriptPath: '../../algorithms',
						args: ['usercf', u, '15']
					};	
					//var u = req.user.personal.id;
					var options2 = {
						scriptPath: '../../algorithms',
						args: ['itemcf', u, '15']
					};
					PythonShell.run('recommendations.py', options1, function (err1, usercf) {
						if (err1) throw err1;
				  	PythonShell.run('recommendations.py',options2,function(err2, itemcf) {
				  	    if (err2) throw err2;
		  	    		res.render('myrecs',{'movies': JSON.parse(usercf),'movies1':JSON.parse(itemcf),'user' : req.user.personal.id});
				  	});
					});
		  	    }	
		var u = req.user.personal.id;
		});
	});
/*see all ibcf */
router.get('/seeallibcf',isAuthenticated, function(req, res){
		var u = req.user.personal.id;
		var options = {
		  scriptPath: '../../algorithms',
		  args: ['itemcf', u, '100']
		};
		  	PythonShell.run('recommendations.py',options,function(err2, itemcf) {
		  	    if (err2) throw err2;
		  	    res.render('seeallibcf',{'movies':JSON.parse(itemcf),'user' : req.user.personal.id});
		  	});
			//res.render('home', { user: req.user });
	});
	
/*see looged users ratings */
router.get('/myratings',isAuthenticated, function(req, res){
		var u = req.user.personal.id;
		var options = {
		  scriptPath: '../../algorithms',
		  args: [u]
		};
		  	PythonShell.run('myratings.py',options,function(err2, rmovies) {
		  	    if (err2) throw err2;
		  	    console.log(rmovies);
		  	    res.render('myratings',{'movies':JSON.parse(rmovies),'user' : req.user.personal.id});
		  	});
			//res.render('home', { user: req.user });
	});
		
/*get Home Page */
router.get('/home',isAuthenticated, function(req, res){
		var options = {
		  scriptPath: '../../algorithms',
		  args: ['25']
		};
		PythonShell.run('wilson.py',options,function(err2, wilsonrated) {
		  	    if (err2) throw err2;
		  	    res.render('index',{'movies':JSON.parse(wilsonrated),'user' : req.user.personal.id});
		  	});
		
});

/*see all wilson */
router.get('/seeallwilson',isAuthenticated, function(req, res){
		var options = {
		  scriptPath: '../../algorithms',
		  args: ['100']
		};
		  	PythonShell.run('wilson.py',options,function(err2, wilsonrated) {
		  	    if (err2) throw err2;
		  	    res.render('seeallwilson',{'movies':JSON.parse(wilsonrated),'user' : req.user.personal.id});
		  	});
			//res.render('home', { user: req.user });
	});
/*see all ubcf */
router.get('/seeallubcf',isAuthenticated, function(req, res){
		var u = req.user.personal.id;
		var options = {
		  scriptPath: '../../algorithms',
		  args: ['usercf', u, '100']
		};
		  	PythonShell.run('recommendations.py',options,function(err2, usercf) {
		  	    if (err2) throw err2;
		  	    console.log(usercf);
		  	    res.render('seeallubcf',{'movies':JSON.parse(usercf),'user' : req.user.personal.id});
		  	});
			//res.render('home', { user: req.user });
	});

	/* Handle Logout */
	router.get('/signout', function(req, res) {
		req.logout();
		res.redirect('/');
	});

	// route for facebook authentication and login
	// different scopes while logging in
	router.get('/login/facebook', 
		passport.authenticate('facebook', { scope : 'email' }
	));

	// handle the callback after facebook has authenticated the user
	router.get('/login/facebook/callback',
		passport.authenticate('facebook', {
			successRedirect : '/home',
			failureRedirect : '/'
		})
	);

	// route for twitter authentication and login
	// different scopes while logging in
	router.get('/login/twitter', 
		passport.authenticate('twitter'));

	// handle the callback after facebook has authenticated the user
	router.get('/login/twitter/callback',
		passport.authenticate('twitter', {
			successRedirect : '/twitter',
			failureRedirect : '/'
		})
	);

	/* GET Twitter View Page */
	router.get('/twitter', isAuthenticated, function(req, res){
		res.render('twitter', { user: req.user });
	});
    
    router.get('/auth/google', passport.authenticate('google', { scope : ['profile', 'email'] }));

    // the callback after google has authenticated the user
    router.get('/login/google/callback',
            passport.authenticate('google', {
                    successRedirect : '/',
                    failureRedirect : '/'
            }));
    router.get('/api/suggestions/json', function(req,res){
	  var options = {
		  scriptPath: '../../algorithms',
		  args: ['usercf', '1', '10']
		};
		PythonShell.run('recommendations.py', options, function (err, results) {
		  if (err) throw err;
		  	//res.json({'message': 'Some error occured!!','code': 502});
		  res.json(JSON.parse(results));
		});
	});
	router.post('/user/rate',function(req, res) {
	   console.log(req.body);
	   var txt = "\n"+req.body.alias+"\t"+req.body.movie_id+"\t"+req.body.rate+"\t123456789";
	   fs.appendFile('../../algorithms/ml-100k/u.data', txt, function (err) {
		  if (err){ 
		  	throw err
		  	res.json({'status':'error'});
		  }else{
		  	  var newMovie = new Movie();
		  	  newMovie.user_id = req.body.alias;
		  	  newMovie.movie_id = req.body.movie_id;
		  	  newMovie.rating = req.body.rate;
		  	  newMovie.save(function(err) {
	                    if (err)
	                        throw err;
						 var options = {
							  scriptPath: '../../algorithms',
							};
							PythonShell.run('similaritems.py', options, function (err, results) {
							  if (err) throw err;
							  	//res.json({'message': 'Some error occured!!','code': 502});
								console.log("Matrix updated!!");
	                    		console.log("Saved Movie Ranking Successfully!!");
								console.log('The "data to append" was appended to file!');
								res.json({'status' : 'success'});
							});
	                    // if successful, return the new user	                    
	                });
		  }
		});
	});
	
	router.get('/movie_details/',function(req, res) {
	   var a= req.query.a;
	   var y= req.query.y;
	   if(a==null || y==null || typeof a =='undefined' || typeof y =='undefined' || a=='' || y==''){
	   	res.send('Incomplete Query!!');
	   }
	   else{
	   	var url="http://www.omdbapi.com/?t="+a+"&y="+y+"&plot=full&r=json";
	   	request(url, function (error, response, body) {
		  if (!error && response.statusCode == 200) {
		    res.render('single',{'movie':JSON.parse(body)}); // Show the HTML for the Google homepage. 
		  }else{
		  	console.log(error.stack);
		  	res.status(error.status||500).send('Something is broken!!');
		  }
		});
	   }
	});
	return router;
}