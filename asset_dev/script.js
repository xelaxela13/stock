var lFollowX = 0,
    lFollowY = 0,
    x = 0,
    y = 0,
    friction = 1 / 30;

function moveElement() {
    x += (lFollowX - x) * friction;
    y += (lFollowY - y) * friction;

    let translate = 'translate(' + x + 'px, ' + y + 'px) scale(1.1)';

    $('.ktp').css({
        '-webit-transform': translate,
        '-moz-transform': translate,
        'transform': translate
    });
    window.requestAnimationFrame(moveElement);
}

$.fn.isInViewport = function () {
    let elementTop = $(this).offset().top,
        elementBottom = elementTop + $(this).outerHeight(),
        viewportTop = $(window).scrollTop(),
        viewportBottom = viewportTop + $(window).height();
    return elementBottom > viewportTop && elementTop < viewportBottom;
};

$(window).on('mousemove click', function (e) {
    let lMouseX = Math.max(-100, Math.min(100, $(window).width() / 2 - e.clientX));
    let lMouseY = Math.max(-100, Math.min(100, $(window).height() / 2 - e.clientY));
    lFollowX = (20 * lMouseX) / 100; // 100 : 12 = lMouxeX : lFollow
    lFollowY = (10 * lMouseY) / 100;
});

function backgroundSize(el, size) {
    let wst = $(window).scrollTop(), element = $(el), elementHeight = element.height(),
        elementBgSize = size - ((wst * 100 / elementHeight) * 100 / size);
    element.isInViewport() && elementBgSize > 100 &&
    $(element).css('background-size', elementBgSize + '%')
}

function backgroundPosition(el, position) {
    let wst = $(window).scrollTop(), element = $(el), elementHeight = element.height(),
        elementPosition = position - ((wst * 100 / elementHeight) * 100 / position) * 3;
    element.isInViewport() && $(element).css('background-position-y', elementPosition + 'px')
}

// $(document).on('scroll', function () {
//     backgroundSize('.bg-section-first', 130);
//     backgroundPosition('.bg-section-solar', 400);
// });

function activatePopover(element, placement) {
    $(element).length &&
    $(element).popover(
        {
            trigger: 'hover',
            placement: placement,
        }
    )
}

function offsetBottom(element) {
    return $(element).offset().top + $(element).height();
}

function scrollToElement(element, speed, offset) {
    speed = speed ? speed : 100;
    offset = offset ? offset : 0;
    $('html, body').animate({scrollTop: $(element).offset().top - offset}, speed);
}

function scrollToSection(section) {
    let offset = $(section).prev().offset().top;
    console.log(offset, offset - 100, window.pageYOffset)
    if ($(section).isInViewport() && window.pageYOffset < offset && window.pageYOffset > offset - 50) {
        scrollToElement(section);
    }
}

function animateBlocks() {
    $(window).on('scroll', function () {
        $('.solar-animate-1').isInViewport() && $('.solar-animate-1').css('opacity', '1').addClass('slideLeftReturn');
        $('.docs-animate-1').isInViewport() && $('.docs-animate-1').css('opacity', '1').addClass('slideLeftReturn');
        $('.docs-animate-2').isInViewport() && $('.docs-animate-2').css('opacity', '1').addClass('slideLeftReturn');
        $('.docs-animate-3').isInViewport() && $('.docs-animate-3 img').css('opacity', '1').addClass('puffIn');
    })
}

function activateSlick(element) {
    $(element).slick(
        {
            dots: false,
            infinite: true,
            speed: 300,
            slidesToShow: 5,
            centerMode: true,
            centerPadding: '20px',
            prevArrow: '<div class="slick-prev shadow"><span class="oi oi-caret-left"></span></div>',
            nextArrow: '<div class="slick-next shadow"><span class="oi oi-caret-right"></span></div>',
            responsive: [
                {
                    breakpoint: 768,
                    settings: {
                        arrows: false,
                        slidesToShow: 1
                    }
                }
            ]
        }
    )
}
