(function ($) {
    $(function () {
        let styles = {
            'width': '100%'
        };
        $('.related-widget-wrapper span.select2.select2-container--jet').css(styles);
        $('.related-widget-wrapper span.select2').click(() => {
            $('ul.select2-results__options').css({'display': 'inline-flex', 'flex-wrap': 'wrap'});
            $('li.select2-results__option').map((index, element) => {
                let styles = {
                    'background': 'url("/media/' + $(element).text() + '")',
                    'width': '50px',
                    'height': '50px',
                    'background-size': 'cover',
                    'margin': '.5rem',
                    'list-style-type': 'none',
                };
                $(element).attr('aria-selected') === 'true' && Object.assign(styles,{'border': '1px solid red'});
                $(element).css(styles).html('');
            })
        })
    })
})(django.jQuery);