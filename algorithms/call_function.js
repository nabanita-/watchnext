/*var spawn = require("child_process").spawn;
var process = spawn('python',["recommendations.py",'usercf','1','20']);

process.stdout.on('data', function (data) {
  console.log('stdout: ' + data);
});
*/
var PythonShell = require('python-shell');
 
var options = {
  //mode: 'json',
  args: ['usercf', '1', '10']
};
 
var pyshell = new PythonShell('recommendations.py', options); 

pyshell.stdout.on('data', function(data) {
    //var newdata=JSON.parse(data);
    console.log(data);
    //console.log(data[1]);
    
});

