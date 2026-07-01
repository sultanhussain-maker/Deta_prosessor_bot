# app/core/pdfgen.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_pdf(report_text, watermark="DataCleaner Pro"):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont("Helvetica", 12)
    t = c.beginText(40, 800)
    for line in report_text.split("\n"):
        t.textLine(line)
    c.drawText(t)
    c.setFont("Helvetica", 40)
    c.setFillGray(0.85)
    c.drawString(150, 400, watermark)
    c.save()
    buf.seek(0)
    return buf