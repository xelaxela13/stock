from html import escape
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.utils.six import BytesIO, StringIO


class PDFTemplateResponse(TemplateResponse):

    def generate_pdf(self, *args, **kwargs):
        html = BytesIO(self.content)
        result = BytesIO()
        rendering = pisa.pisaDocument(html, result, encoding='utf-8')

        if rendering.err:
            return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
        else:
            self.content = result.getvalue()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, content_type='application/pdf', **kwargs)
        self.add_post_render_callback(self.generate_pdf)


class PDFTemplateView(TemplateView):
    response_class = PDFTemplateResponse
    content_type = "application/pdf"
