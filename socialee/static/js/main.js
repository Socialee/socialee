$(document).ready(function() {
  $(document).foundation({
      offcanvas : {
      // Sets method in which offcanvas opens.
      // [ move | overlap_single | overlap ]
      open_method: 'move', 
      // Should the menu close when a menu link is clicked?
      // [ true | false ]
      close_on_click : false
    }
  });

  $('.socialee-lp-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    speed: 3000,
    arrows: false,
    fade: true,
  });

  $('.socialee-project-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 4000,
    speed: 4000,
    arrows: false,
    fade: false,
  });

  $('.zettel-slide-left').slick({
    slidesToShow: 1,
    vertical: true,
    verticalSwiping: true,
    slidesToScroll: 1,
    autoplay: false,
    autoplaySpeed: 3000,
    speed: 2000,
    arrows: true,
    prevArrow: '#navtopleft',
    nextArrow: '#navbottomleft',
  });

  $('.zettel-slide-right').slick({
    slidesToShow: 1,
    vertical: true,
    verticalSwiping: true,
    slidesToScroll: 1,
    autoplay: false,
    autoplaySpeed: 3000,
    speed: 2000,
    arrows: true,
    prevArrow: '#navtopright',
    nextArrow: '#navbottomright',
  });

  $('.socialee-cafe-bg-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    speed: 3000,
    arrows: false,
    fade: true,
  });

  $('.cafePromoSlider').slick({
  centerMode: true,
  centerPadding: '0px',
  slidesToShow: 3,
  responsive: [
    {
      breakpoint: 768,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '10px',
        slidesToShow: 1
      }
    },
    {
      breakpoint: 480,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '10px',
        slidesToShow: 1
      }
    }
  ]
  });
});