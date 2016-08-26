// this blog.js is being loaded in base.html before closing body tag, treat it well

$(document).ready(function(){

  var now = new Date();
  var hours = now.getHours();
  var msg;
  if ( hours > 5 && hours < 11 ) msg = "Einen schönen guten Morgen beim Socialee Blog.";
  else if (hours < 14) msg = "Einen schönen guten Mittag beim Socialee Blog.";
  else if (hours < 18) msg = "Einen schönen guten Tag beim Socialee Blog.";
  else if (hours < 23) msg = "Einen schönen guten Abend beim Socialee Blog.";
  else msg = "Es ist schon spät, noch einen Artikel und ab ins Bett!";

  $("#daytime").html(msg);   
});
