import time, os, sys, csv, pyautogui, urllib.parse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv("config/.env")
ESPERA_WHATSAPP = int(os.getenv("ESPERA_WHATSAPP", 15))
URL_SISTEMA     = os.getenv("URL_SISTEMA", "http://127.0.0.1:5000")
NOME_EMPRESA    = os.getenv("NOME_EMPRESA", "TechSolutions Ltda")
ARQUIVO_ERROS   = "dados/erros.csv"
PASTA_BOLETOS   = "boletos"

sys.path.insert(0, "1parte_web")
from database import listar_faturas_pendentes, atualizar_status_fatura

def validar_telefone(tel):
    limpo = "".join(c for c in str(tel) if c.isdigit())
    return len(limpo) >= 12, limpo

def montar_mensagem(fatura):
    nome_arq    = f"boleto_cliente{fatura['id']:03d}_{fatura['nome'].replace(' ','_')}.pdf"
    link_boleto = f"{URL_SISTEMA}/boletos/{nome_arq}"
    return (
        f"Olá, *{fatura['nome']}*! 👋\n\n"
        f"Notificação automática da *{NOME_EMPRESA}*.\n\n"
        f"📄 *Fatura #{fatura['id']:05d}*\n"
        f"💰 Valor: *R$ {fatura['valor']:.2f}*\n"
        f"📅 Vencimento: *{fatura['data_vencimento']}*\n\n"
        f"Pague pelo QR Code PIX:\n🔗 {link_boleto}\n\n"
        f"Dúvidas? Responda esta mensagem.\n"
        f"_{NOME_EMPRESA} — Financeiro_ 🏢"
    )

def registrar_erro(fatura, erro):
    os.makedirs("dados", exist_ok=True)
    existe = os.path.exists(ARQUIVO_ERROS)
    with open(ARQUIVO_ERROS, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not existe:
            w.writerow(["fatura_id", "cliente", "erro", "data_hora"])
        w.writerow([fatura["id"], fatura["nome"], erro,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

def enviar_whatsapp(driver, fatura):
    valido, telefone = validar_telefone(fatura["telefone"])
    if not valido:
        raise ValueError(f"Telefone inválido: {fatura['telefone']}")

    url = f"https://web.whatsapp.com/send?phone={telefone}&text={urllib.parse.quote(montar_mensagem(fatura))}"
    print(f"   🌐 Abrindo WhatsApp para {fatura['nome']} ({telefone})...")
    driver.get(url)

    wait = WebDriverWait(driver, 40)
    caixa = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@title="Digite uma mensagem"]'))
    )
    time.sleep(2)
    caixa.click()
    time.sleep(0.5)
    pyautogui.hotkey("enter")
    time.sleep(2)
    print(f"   ✅ Enviado para {fatura['nome']}!")

def main():
    print("=" * 50)
    print("  📱 RPA - Envio via WhatsApp Web")
    print("=" * 50)

    faturas = listar_faturas_pendentes()
    if not faturas:
        print("⚠️  Nenhuma fatura pendente.")
        return

    print(f"\n📋 {len(faturas)} fatura(s) para enviar\n")

    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    # Descomente para manter sessão entre execuções:
    # opcoes.add_argument("--user-data-dir=./whatsapp_session")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opcoes
    )

    try:
        print(f"📱 Abrindo WhatsApp Web...")
        print(f"   ⏳ Você tem {ESPERA_WHATSAPP}s para escanear o QR Code!")
        driver.get("https://web.whatsapp.com")
        time.sleep(ESPERA_WHATSAPP)

        enviados = falhas = 0
        for i, f in enumerate(faturas, 1):
            print(f"\n[{i}/{len(faturas)}] {f['nome']} — R$ {f['valor']:.2f}")
            try:
                enviar_whatsapp(driver, f)
                atualizar_status_fatura(f["id"], "enviado")
                enviados += 1
            except Exception as e:
                print(f"   ❌ ERRO: {e}")
                registrar_erro(f, str(e))
                atualizar_status_fatura(f["id"], "falhou")
                falhas += 1
            time.sleep(3)
    finally:
        driver.quit()

    print(f"\n{'='*50}")
    print(f"✅ Enviados: {enviados} | ❌ Falhas: {falhas}")
    if falhas: print(f"📄 Erros em: {ARQUIVO_ERROS}")

if __name__ == "__main__":
    main()