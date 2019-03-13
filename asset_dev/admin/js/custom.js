(function ($) {
    $(function () {
       $(['input:not(.action-select)', 'td:not(.delete) input']).each(function () {
           $(this).css('display', 'inline');
       })
    })
})(django.jQuery);