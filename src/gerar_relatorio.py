from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Importar texto consolidado
with open("resultados.txt", "r", encoding="utf-8") as f:
    conteudo = f.read()

pdf.multi_cell(0, 10, conteudo)

# Salvar PDF
pdf.output("Relatorio_Final.pdf")
