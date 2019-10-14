var lFollowX = 0,
    lFollowY = 0,
    x = 0,
    y = 0,
    friction = 1 / 30;

function moveElement() {
    x += (lFollowX - x) * friction;
    y += (lFollowY - y) * friction;

    translate = 'translate(' + x + 'px, ' + y + 'px) scale(1.1)';

    $('.ktp').css({
        '-webit-transform': translate,
        '-moz-transform': translate,
        'transform': translate
    });
    window.requestAnimationFrame(moveElement);
}

$(window).on('mousemove click', function (e) {
    var lMouseX = Math.max(-100, Math.min(100, $(window).width() / 2 - e.clientX));
    var lMouseY = Math.max(-100, Math.min(100, $(window).height() / 2 - e.clientY));
    lFollowX = (20 * lMouseX) / 100; // 100 : 12 = lMouxeX : lFollow
    lFollowY = (10 * lMouseY) / 100;
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
    $('html, body').animate({ scrollTop: $(element).offset().top }, speed);
}

function animateBlocks() {
    var flag = true;
    $(window).on('scroll', function () {
        $('.fill-path-right').addClass('slideRightReturn d-lg-block');
        setTimeout(() => {
            $('.block-02').css('opacity', '1').addClass('slideLeftReturn')
        }, 1000);
        if (this.pageYOffset >= $('.solar-bg').offset().top && flag) {
            scrollTo('#stab');
            flag = false;
        }
    })
}