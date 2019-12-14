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

$(document).on('scroll', function () {
    let wst = $(window).scrollTop(), element = $('.bg-section-first'), elementHeight = element.height(),
        elementBgSize = 130 - ((wst * 100 / elementHeight) * 100 / 130);
    element.isInViewport() && elementBgSize > 100 &&
        element.css('background-size', elementBgSize + '%')
});

function activatePopover(element, content, placement) {
    $(element).length &&
    $(element).popover(
        {
            trigger: 'hover',
            placement: placement,
            content: content
        }
    )
}

function offsetBottom(element) {
    return $(element).offset().top + $(element).height();
}

function scrollTo(element, speed) {
    speed = speed ? speed : 100;
    $('html, body').animate({scrollTop: $(element).offset().top}, speed);
}

function scrollToSection(section) {
    let offset = $(section).prev().offset().top;
    if ($(section).isInViewport() && window.pageYOffset < offset && window.pageYOffset > offset - 100) {
            scrollTo(section);
        }
}

function animateBlocks() {
    // var flag = true;
    $(window).on('scroll', function () {
        $('.fill-path-right').addClass('slideRightReturn d-lg-block');
        setTimeout(() => {
            $('.block-02').css('opacity', '1').addClass('slideLeftReturn')
        }, 1000);
        // if (this.pageYOffset >= $('.bg-section-solar').offset().top && flag) {
        //     scrollTo('#stab');
        //     flag = false;
        // }
        scrollToSection('#stab')
    })
}