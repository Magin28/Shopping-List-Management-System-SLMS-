from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def export_to_txt(list_name, products, file_path):
    content = f"Lista zakupów: {list_name}\n\n"
    for idx, product in enumerate(products, 1):
        content += f"{idx}. {product.name} ({product.category})\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def export_to_pdf(list_name, products, file_path):
    pdf = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 50, f"Lista zakupów: {list_name}")

    data = [["Lp.", "Produkt", "Kategoria"]]
    for idx, product in enumerate(products, 1):
        data.append([str(idx), product.name, product.category])

    table = Table(data, colWidths=[50, 300, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#bdc3c7"))
    ]))

    table.wrapOn(pdf, width - 100, height)
    table.drawOn(pdf, 50, height - 150)
    pdf.save()