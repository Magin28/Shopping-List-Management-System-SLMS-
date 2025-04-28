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