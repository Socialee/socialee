(function ( $ ) {

    $(document).ready( function() {

    });

    $(window).resize(function(){

        if($('.hidden-xs:first').is(':hidden')) return false;

        var mrg_t = $(window).height();
        var win_w = $(window).width();
        var win_h = $(window).height();

        if($('.fixed:first').css('position') !== 'fixed')
        {
            var el_w = el_h = el_t = 0;

            //if(mrg_t > win_h)
            //    el_t = win_h - mrg_t - 72;


            $('header, section, footer').css({
                position: 'relative',
                top: 'auto'
            }).each(function(i){

                var el = $(this);

                if(el.hasClass('jumpage'))
                el_t += $(window).height();

                el_h = el.height();
                el_w = el.width();

                el.data('top', el_t).css({
                    position: 'absolute',
                    zIndex: 100 + i,
                    top: el_t,
                    left: el.offset().left
                });

                el_t += el_h;
            });

            $('.video_placeholder').remove();
        }
        else
        {
            $('section:first').css({
                marginTop: mrg_t
            });
        }

    });

    $(window).load(function(){

        if($('.hidden-xs:first').is(':hidden')) return false;

        if($('.fixed:first').css('position') !== 'fixed')
        {
            $(window).trigger('resize').scroll(function(){
                var scrollTop =  $(document).scrollTop();
                if(scrollTop < $(document).height() - $(window).height())
                {
                    $('section, footer').each(function(){
                        var el = $(this);
                        var el_t = el.data('top');
                        var scroll_t = el_t - scrollTop;

                        el.css({
                            top: scroll_t
                        })
                    });
                }
            });
        }
        else
        {
            $(window).trigger('resize');
        }
    });

    $.fn.jumpage = function() {
        return this;
    };

}( jQuery ));