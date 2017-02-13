// this main.js is being loaded in base.html before closing body tag, treat it well

// Foundation
$(document).foundation();

$(document).ready(function(){

  $(".js-content-sized").each(fixSizedElements);
  $('.input_with_bound').each(setLimit);
  $('.input_with_bound').bind('input propertychange', setLimit);
  $(".input_with_img").change(function(){ readURLInputIntoImg(this); } );
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

function follow(object, instance_id) {
    post_to_url( "/follow/",
                { instance_id : instance_id },
                function(data){
                    object.replaceWith(data);
                });
};

$(document).on("click", ".follow", function(event) {
    follow($(this), $(this).attr('instance_id'))
 });



function showOnlyIfFit() {
    var height = $(this).parent(".js-content-sized").position().top + $(this).parent(".js-content-sized").outerHeight(true);
    console.log((this.parentElement.offsetHeight)+"/" + (this.offsetTop + this.offsetHeight));
    $(this).toggle(this.offsetTop + this.offsetHeight < height);
}

function fixSizedElements()
{
    $(this).children(".js-sized").each(showOnlyIfFit);
    $(this).find(".js-sized-more").hide();
    var diff = $(this).children(".js-sized").length - $(this).children(".js-sized:visible").length
    if ( diff>0 )
    { 
        $(this).children(".js-sized:visible").last().hide();
        $(this).children(".js-sized-more").html("<i class='fa fa-plus'></i> "+(diff+1)+" Mehr");
        $(this).children(".js-sized-more").show();
        $(this).children(".js-sized-more").on("click", function() {
            $(this).parent(".js-content-sized").children(".js-sized").show();
            $(this).hide();
        });
    }
}

function setLimit() {
  var max = $(this).attr("max_length");
  if($(this).val().length > max)
  {
    $(this).val($(this).val().substring(0,max));
  }
  var num = max-$(this).val().length;
  var $label = $("label[for='"+this.id+"']");
  $label.html(num +" Zeichen übrig");
  if(num == 0)
    $label.css('color', 'red');
  else 
    $label.css('color', 'grey');
}


function readURLInputIntoImg(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
          $(input).parents("fieldset").first().find("img").attr("src", e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}


