jQuery(document).ready(function () {
    // signup form
    const phone_field = $('#id_phone');
    if (phone_field.length > 0) {
        phone_field.mask('+380(99)9999999');
    }

    const form_group = $('.form-group');
    form_group.each(function () {
        if ($(this).children('small').length > 0) {
            $(this).append('<span class="help-tooltip">?</span>');
        }

    });

    const help_tooltip = $('.help-tooltip');
    help_tooltip.mouseover(function (e) {
        $(this).prev('small').fadeIn(100);
    });
    help_tooltip.mouseout(function (e) {
        $(this).prev('small').fadeOut();
    });

    // messages notification
    const messages = $('.alert');
    if (messages.length > 0) {
        const messages_height = messages.outerHeight();
        var pos = messages.position().top;
        $.each(messages, function (index, element) {
            if (index > 0) {
                pos += messages_height + 10;
                $(element).css('top', pos);
            }
        });
        window.setTimeout(function () {
            messages.fadeTo(500, 0).slideUp(500, function () {
                $(this).remove();
            });
        }, 4000);
    }

    // animate vertical line and circles
    const circle = $(".circle"),
        vertical_line = $('.vertical_line');
    circle.on('mouseover', function (e) {
        vertical_line.addClass('bold');
        var closest_text_block = $(this).closest('.row').find('.border_bottom_dashed');
        closest_text_block.addClass('closest_text_block_show');
        closest_text_block.removeClass('closest_text_block_hide')
    });
    circle.on('mouseout', function (e) {
        vertical_line.removeClass('bold');
        var closest_text_block = $(this).closest('.row').find('.border_bottom_dashed');
        closest_text_block.removeClass('closest_text_block_show');
        closest_text_block.addClass('closest_text_block_hide')
    });

    // if element view on screen
    var description = $('.row .col-lg-4.border_bottom_dashed'),
        solar_panel_bg = $('.solar_panel_bg'),
        solar_panel_text = $('.solar_panel_text');
    $(window).scroll(function () {
        description.each(function () {
            if (Utils.isElementInView($(this))) {
                description.css('opacity', '1');
                return false;
            }
        });
        if (solar_panel_bg.length > 0){
            if (Utils.isElementInView(solar_panel_bg, true) || Utils.isElementInView(solar_panel_text, true)) {
                solar_panel_bg.css('opacity', '1');
                solar_panel_text.css('opacity', '1');
            }
        }

    });

});