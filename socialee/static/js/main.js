// this main.js is being loaded in base.html before closing body tag, treat it well

// Foundation
$(document).foundation();

// Slick Slider
$(document).ready(function(){
  
  $('.project-header-slider').slick({
  	slidesToShow: 1,
  	dots: false,
  	arrows: false,
  	autoplay: true,
  	autoplaySpeed: 5000,
  	fade: true,
  });

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


function change_socialeebhaber(id, user_id) {
    $.ajax({
    	beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    },
        url : "/" + user_id + "/socialeebhaber/", // the endpoint
        type : "POST", // http method
        data : { project_id : id}, // data sent with the post request

        // handle a successful response
        success : function(data) {
            $('#'+id).html(data);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};


$(document).on("dblclick", ".socialeebhaber", function(event) {
     change_socialeebhaber($(this).attr('id'), $(this).attr('user_id'))
 });
