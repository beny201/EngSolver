import base64
import io
from io import BytesIO
from typing import Dict

from django.http import HttpResponse
from django.template.loader import get_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from xhtml2pdf import pisa


def creating_graph(*args):
    fig = Figure(figsize=(3, 3), dpi=140)
    plot1 = fig.add_subplot(111)

    for line in args:
        plot1.plot(*line.xy)

    plot1.axis('equal')
    canvas = FigureCanvas(fig)
    buffer = io.BytesIO()
    canvas.print_png(buffer)
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    return image_data


def render_to_pdf(template_src: str, context_dict: Dict, filename: str):
    name = f'{filename}/pdf'
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename={name}'
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type="text/plain")
    return response
