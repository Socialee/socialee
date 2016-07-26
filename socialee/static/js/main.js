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