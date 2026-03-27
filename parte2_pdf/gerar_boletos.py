import os, sys, qrcode
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from dotenv import load_dotenv

load_dotenv("config/.env")
PASTA_BOLETOS = "boletos"
NOME_EMPRESA  = os.getenv("NOME_EMPRESA", "TechSolutions Ltda")

sys.path.insert(0, "1parte_web")
from database import listar_faturas_pendentes

def gerar_qr_code(fatura):
    nome_cliente = str(fatura.get("nome", "")).replace("|", " ").strip()
    payload = (
        f"PIX|{NOME_EMPRESA}|Cliente:{nome_cliente}|Fatura#{fatura['id']}"
        f"|Valor:R${fatura['valor']:.2f}|Venc:{fatura['data_vencimento']}"
    )
    qr  = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def gerar_codigo_barras(fatura_id, valor):
    import random
    random.seed(fatura_id)
    return (f"0001.{fatura_id:04d} {valor:.0f}00.0 "
            f"{random.randint(10000,99999)}.{random.randint(100000,999999)} "
            f"{random.randint(1,9)} {random.randint(10**13, 10**14-1)}")

def gerar_boleto_pdf(fatura, caminho_saida):
    c = canvas.Canvas(caminho_saida, pagesize=A4)
    w, h = A4

    # Cabeçalho
    c.setFillColor(colors.HexColor("#1a237e"))
    c.rect(0, h - 3*cm, w, 3*cm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w/2, h - 1.5*cm, NOME_EMPRESA)
    c.setFont("Helvetica", 10)
    c.drawCentredString(w/2, h - 2.2*cm, "BOLETO DE COBRANÇA")
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(w - 1.5*cm, h - 1.5*cm, f"Fatura Nº {fatura['id']:05d}")

    # Dados cliente
    y = h - 4.5*cm
    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1.5*cm, y, "DADOS DO CLIENTE")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    for campo in [f"Nome:     {fatura['nome']}", f"E-mail:   {fatura['email']}", f"Telefone: {fatura['telefone']}"]:
        y -= 0.6*cm
        c.drawString(1.5*cm, y, campo)

    # Separador
    y -= 0.5*cm
    c.setStrokeColor(colors.HexColor("#1a237e"))
    c.setLineWidth(1.5)
    c.line(1.5*cm, y, w - 1.5*cm, y)

    # Dados boleto
    y -= 0.8*cm
    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1.5*cm, y, "DADOS DO BOLETO")
    y -= 0.7*cm
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.5*cm, y, f"Valor:   R$ {fatura['valor']:.2f}")
    y -= 0.6*cm
    c.setFont("Helvetica", 11)
    c.drawString(1.5*cm, y, f"Vencimento:      {fatura['data_vencimento']}")
    y -= 0.5*cm
    c.drawString(1.5*cm, y, f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y')}")

    # Código de barras
    y -= 1*cm
    c.setFillColor(colors.HexColor("#f5f5f5"))
    c.rect(1.5*cm, y - 0.3*cm, w - 3*cm, 0.9*cm, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Courier", 9)
    c.drawCentredString(w/2, y + 0.1*cm, gerar_codigo_barras(fatura['id'], fatura['valor']))
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(w/2, y - 0.5*cm, "Linha digitável")

    # QR Code
    y -= 2.5*cm
    qr_buf = gerar_qr_code(fatura)
    qr_img = ImageReader(qr_buf)
    qr_x   = w/2 - 2.5*cm
    c.drawImage(qr_img, qr_x, y - 4*cm, width=5*cm, height=5*cm)
    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(w/2, y + 0.3*cm, "📱 Pague via PIX — Escaneie o QR Code")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w/2, y - 4.5*cm, "Leia com o app do seu banco")

    # Rodapé
    c.setFillColor(colors.HexColor("#1a237e"))
    c.rect(0, 0, w, 1.5*cm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w/2, 0.6*cm,
        f"{NOME_EMPRESA} | Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.save()
    print(f"   ✅ {caminho_saida}")

def main():
    print("=" * 50)
    print("  📄 Geração de Boletos em PDF + QR Code")
    print("=" * 50)

    os.makedirs(PASTA_BOLETOS, exist_ok=True)
    faturas = listar_faturas_pendentes()

    if not faturas:
        print("⚠️  Nenhuma fatura pendente. Cadastre no sistema web primeiro!")
        return

    print(f"\n📋 {len(faturas)} fatura(s) encontrada(s). Gerando PDFs...\n")
    for f in faturas:
        nome_arq = f"boleto_cliente{f['id']:03d}_{f['nome'].replace(' ','_')}.pdf"
        print(f"[{f['id']}] {f['nome']} — R$ {f['valor']:.2f}")
        gerar_boleto_pdf(f, os.path.join(PASTA_BOLETOS, nome_arq))

    print(f"\n✅ {len(faturas)} boleto(s) gerado(s) em '{PASTA_BOLETOS}/'")

if __name__ == "__main__":
    main()