$('.tweeter_login').click(function(e){
  $.ajax({
      url:'api.twitter.com/oauth/request_token',
      type: 'post',
      success : function(res){
          //thamlam
      }
  })  
}); 