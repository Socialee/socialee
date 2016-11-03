// this main.js is being loaded in base.html before closing body tag, treat it well

// Foundation
$(document).foundation();

$(document).ready(function(){

  $('a[href^="#"]').on('click',function (e) {
	    e.preventDefault();

	    var target = this.hash;
	    var $target = $(target);

	    $('html, body').stop().animate({
	        'scrollTop': $target.offset().top
	    }, 1200, 'swing', function () {
	        window.location.hash = target;
	    });
	});
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function post_to_url(url, data, success_fct)
{
    $.ajax({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url : url, // the endpoint
        type : "POST", // http method
        data : data, // data sent with the post request

        // handle a successful response
        success : success_fct,

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function post_comment(comment, instance_id, reply_id) {
    post_to_url( "/comment/", 
                { comment : comment,
                instance_id: instance_id,
                reply_id: reply_id },
                function(data){
                    $('#object'+instance_id).children().first().after(data);
                });
};

function follow(object, instance_id) {
    post_to_url( "/follow/", 
                { instance_id : instance_id },
                function(data){
                    object.replaceWith(data);
                });
};

$(document).on("click", ".comment_button", function(event) {
     post_comment($("#comment_value").val(), $(this).attr('instance_id'), $(this).attr('message_id'))
 });

$(document).on("click", ".follow", function(event) {
    follow($(this), $(this).attr('instance_id'))
 });


// Start js for cards (idea-gallery and create-idea-forms)
var delay=150; // TODO das hier ist ein quick and dirty workaround....
var $grid = $('.grid').masonry({
  columnWidth: 263,
  gutter: 30,
  itemSelector: '.grid-item',
  fitWidth: true,
  transitionDuration: '1s',
  stagger: 10,
});

$grid.imagesLoaded().progress( function() {
  $grid.masonry('layout');
});

$grid.on( 'click', '.idea-image', function( event ) {
  $( event.currentTarget ).parent().parent('.grid-item').toggleClass('is-expanded');
    setTimeout(function() {
    $grid.masonry();
    }, delay);
});

$(".idea-heart").click(
  function()
  {
    var id = $(this).attr('idea_id');
    like($(this).find("#"+id), id, "like");
  });

$(".idea-money").click(
  function()
  {
    var id = $(this).attr('idea_id');
    like($(this).find("#"+id), id, "money");
  });
$(".idea-hand").click(
  function()
  {
    var id = $(this).attr('idea_id');
    like($(this).find("#"+id), id, "hand");
  });

// ask if user wants to login and rearrange layout
$(".idea-heart").click(
  function()
  {
    var delay=300;
    var id = $(this).attr('idea_id');
    $("#login_"+id).slideToggle();
    setTimeout(function() {
    $grid.masonry('layout');
    }, delay);
  });
