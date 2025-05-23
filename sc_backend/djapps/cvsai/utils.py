import io

from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict, filename):
    """
    Universal function to render template to PDF using xhtml2pdf.
    """
    template = get_template(template_src)

    # Render HTML
    html = template.render(context_dict)

    # Create PDF
    result = io.BytesIO()
    pdf = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    return HttpResponse(
        f'We had some errors generating PDF: <b>{pdf.err}</b>', status=500
    )
