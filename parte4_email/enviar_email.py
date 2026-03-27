import smtplib, os, sys, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("config/.env")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")
NOME_EMPRESA    = os.getenv("NOME_EMPRESA", "TechSolutions Ltda")
PASTA_BOLETOS   = "boletos"

sys.path.insert(0, "1parte_web")
from database import listar_faturas_pendentes, atualizar_status_fatura

os.makedirs("dados", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("dados/email_log.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def montar_html(fatura):
    return f"""
    <html><body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto;">
    <div style="background:linear-gradient(135deg,#1a237e,#283593);padding:25px;text-align:center;border-radius:8px 8px 0 0;">
        <h1 style="color:white;margin:0;">{NOME_EMPRESA}</h1>
        <p style="color:#b3c5ff;margin:5px 0 0;">Notificação de Fatura</p>
    </div>
    <div style="background:#f9f9f9;padding:30px;border:1px solid #ddd;">
        <p>Olá, <strong>{fatura['nome']}</strong>!</p>
        <p>Segue o detalhamento da sua fatura:</p>
        <table style="width:100%;border-collapse:collapse;margin:20px 0;">
            <tr style="background:#1a237e;color:white;">
                <th style="padding:10px;text-align:left;">Campo</th>
                <th style="padding:10px;text-align:left;">Informação</th>
            </tr>
            <tr><td style="padding:10px;border-bottom:1px solid #eee;">Nº Fatura</td>
                <td style="padding:10px;border-bottom:1px solid #eee;"><strong>#{fatura['id']:05d}</strong></td></tr>
            <tr style="background:#f5f5f5;">
                <td style="padding:10px;border-bottom:1px solid #eee;">Valor</td>
                <td style="padding:10px;border-bottom:1px solid #eee;"><strong style="color:#c62828;">R$ {fatura['valor']:.2f}</strong></td></tr>
            <tr><td style="padding:10px;">Vencimento</td>
                <td style="padding:10px;"><strong>{fatura['data_vencimento']}</strong></td></tr>
        </table>
        <p>O boleto com QR Code PIX está <strong>anexado neste e-mail</strong>.</p>
        <div style="background:#fff3cd;border-left:4px solid #ffc107;padding:12px;margin:20px 0;border-radius:4px;">
            ⚠️ <strong>Atenção:</strong> Evite atrasos para não gerar multas.
        </div>
        <p>Atenciosamente,<br><strong>{NOME_EMPRESA}</strong></p>
    </div>
    <div style="background:#1a237e;color:#b3c5ff;padding:15px;text-align:center;font-size:12px;border-radius:0 0 8px 8px;">
        E-mail automático — © {datetime.now().year} {NOME_EMPRESA}
    </div>
    </body></html>"""

def encontrar_boleto(fatura_id, nome):
    esperado = os.path.join(PASTA_BOLETOS, f"boleto_cliente{fatura_id:03d}_{nome.replace(' ','_')}.pdf")
    if os.path.exists(esperado):
        return esperado
    for arq in os.listdir(PASTA_BOLETOS):
        if arq.startswith(f"boleto_cliente{fatura_id:03d}") and arq.endswith(".pdf"):
            return os.path.join(PASTA_BOLETOS, arq)
    return None

def enviar_email(fatura):
    if "@" not in fatura["email"]:
        raise ValueError(f"E-mail inválido: {fatura['email']}")

    msg            = MIMEMultipart("alternative")
    msg["From"]    = f"{NOME_EMPRESA} <{EMAIL_REMETENTE}>"
    msg["To"]      = fatura["email"]
    msg["Subject"] = f"📄 Fatura {NOME_EMPRESA} — Vencimento {fatura['data_vencimento']}"
    msg.attach(MIMEText(montar_html(fatura), "html", "utf-8"))

    boleto = encontrar_boleto(fatura["id"], fatura["nome"])
    if boleto:
        with open(boleto, "rb") as pdf:
            anexo = MIMEApplication(pdf.read(), _subtype="pdf")
            anexo.add_header("Content-Disposition", "attachment",
                             filename=os.path.basename(boleto))
            msg.attach(anexo)
        logging.info(f"   📎 Anexo: {os.path.basename(boleto)}")
    else:
        logging.warning(f"   ⚠️  Boleto não encontrado para fatura #{fatura['id']}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL_REMETENTE, EMAIL_SENHA_APP)
        s.sendmail(EMAIL_REMETENTE, fatura["email"], msg.as_string())

def main():
    print("=" * 50)
    print("  📧 RPA - Envio de E-mails com Boleto")
    print("=" * 50)

    faturas = listar_faturas_pendentes()
    if not faturas:
        print("⚠️  Nenhuma fatura pendente.")
        return

    print(f"\n📋 {len(faturas)} fatura(s) para enviar por e-mail\n")
    enviados = falhas = 0

    for i, f in enumerate(faturas, 1):
        print(f"\n[{i}/{len(faturas)}] {f['nome']} → {f['email']}")
        try:
            enviar_email(f)
            atualizar_status_fatura(f["id"], "enviado")
            logging.info(f"✅ E-mail enviado para {f['nome']}")
            enviados += 1
        except smtplib.SMTPAuthenticationError:
            logging.error("❌ Falha de autenticação! Verifique EMAIL_SENHA_APP no .env")
            falhas += 1
            break
        except Exception as e:
            logging.error(f"❌ Falha para {f['nome']}: {e}")
            atualizar_status_fatura(f["id"], "falhou")
            falhas += 1

    print(f"\n{'='*50}")
    print(f"✅ Enviados: {enviados} | ❌ Falhas: {falhas}")
    print(f"📄 Log em: dados/email_log.txt")

if __name__ == "__main__":
    main()