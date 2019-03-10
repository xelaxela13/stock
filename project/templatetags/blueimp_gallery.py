from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def blueimp_gallery(element_id='links'):
    a = """
    <!-- blueimp Gallery styles -->
    <link rel="stylesheet" href="/static/css/fileupload/blueimp-gallery.min.css">
    <!-- blueimp Gallery script -->
    <script src="/static/js/fileupload/jquery.blueimp-gallery.min.js"></script>
     <!-- The blueimp Gallery widget -->
    <div id="blueimp-gallery" class="blueimp-gallery blueimp-gallery-controls">
        <div class="slides"></div>
        <h3 class="title"></h3>
        <a class="prev">‹</a>
        <a class="next">›</a>
        <a class="close">×</a>
        <a class="play-pause"></a>
        <ol class="indicator"></ol>
    </div>
    <script>"""
    b = "if ($('#{element_id}').length) {{document.getElementById('{element_id}').onclick = function (event)".format(
        element_id=element_id)
    c = """
        {
            event = event || window.event;
            var target = event.target || event.srcElement,
                link = target.src ? target.parentNode : target,
                options = {index: link, event: event},
                links = this.getElementsByTagName('a');
            blueimp.Gallery(links, options);
        };
        }
    </script>
    """
    content = a + b + c
    return mark_safe(content)
