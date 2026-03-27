import FreeSimpleGUI as sg
import subprocess, threading, sys, os

sg.theme("DarkBlue14")

def layout():
    return [
        [sg.Text("🏢 TechSolutions — RPA de Cobrança",
                 font=("Segoe UI",16,"bold"), text_color="#b3c5ff",
                 justification="center", expand_x=True, pad=(0,10))],
        [sg.Frame("📋 Módulos", [
            [sg.Button("🌐 Sistema Web",    key="-WEB-",   size=(16,3), button_color=("#fff","#1a237e")),
             sg.Button("🤖 RPA Cadastro",   key="-RPA-",   size=(16,3), button_color=("#fff","#283593")),
             sg.Button("📄 Gerar Boletos",  key="-PDF-",   size=(16,3), button_color=("#fff","#00695c"))],
            [sg.Button("📱 WhatsApp",       key="-WA-",    size=(16,3), button_color=("#fff","#1b5e20")),
             sg.Button("📧 E-mails",        key="-EMAIL-", size=(16,3), button_color=("#fff","#880e4f")),
             sg.Button("📊 Relatório",      key="-XLS-",   size=(16,3), button_color=("#fff","#4a148c"))],
            [sg.Button("🚀 EXECUTAR TUDO (Partes 2→5)", key="-TUDO-",
                       expand_x=True, size=(50,3), button_color=("#fff","#b71c1c"))]
        ], expand_x=True)],
        [sg.Frame("📟 Log", [[
            sg.Multiline("Aguardando...\n", key="-LOG-", size=(70,15),
                         font=("Courier New",9), background_color="#0d1117",
                         text_color="#58a6ff", autoscroll=True, expand_x=True,
                         disabled=True)
        ]], expand_x=True)],
        [sg.ProgressBar(100, orientation="h", size=(40,15), key="-PROG-", expand_x=True),
         sg.Text("Pronto", key="-ST-", size=(20,1), text_color="#58a6ff")],
        [sg.Button("🗑️ Limpar", key="-LIMPAR-"),
         sg.Button("📂 Pasta Boletos", key="-PASTA-"),
         sg.Push(),
         sg.Button("❌ Sair", key="-SAIR-", button_color=("#fff","#c62828"))]
    ]

SCRIPTS = {
    "-WEB-":  "1parte_web/app.py",
    "-RPA-":  "parte1_rpa/rpa_cadastro.py",
    "-PDF-":  "parte2_pdf/gerar_boletos.py",
    "-WA-":   "parte3_whatsapp/enviar_whatsapp.py",
    "-EMAIL-":"parte4_email/enviar_email.py",
    "-XLS-":  "parte5_relatorio/relatorio_excel.py",
}

def rodar(script, janela, nome):
    def run():
        janela.write_event_value("-START-", nome)
        try:
            r = subprocess.run([sys.executable, script],
                               capture_output=True, text=True, cwd=os.getcwd())
            janela.write_event_value("-DONE-", (nome, r.stdout+r.stderr, r.returncode==0))
        except Exception as e:
            janela.write_event_value("-DONE-", (nome, str(e), False))
    threading.Thread(target=run, daemon=True).start()

def log(janela, txt):
    janela["-LOG-"].update(disabled=False)
    janela["-LOG-"].print(txt)
    janela["-LOG-"].update(disabled=True)

def main():
    win = sg.Window("TechSolutions RPA", layout(), resizable=True,
                    finalize=True, size=(800,620))
    log(win, "🚀 Pronto! Inicie o Sistema Web antes dos outros módulos.\n")

    while True:
        ev, _ = win.read(timeout=100)
        if ev in (sg.WIN_CLOSED, "-SAIR-"):
            break
        elif ev == "-LIMPAR-":
            win["-LOG-"].update(disabled=False)
            win["-LOG-"].update("")
            win["-LOG-"].update(disabled=True)
        elif ev == "-PASTA-":
            pasta = os.path.abspath("boletos")
            os.makedirs(pasta, exist_ok=True)
            os.startfile(pasta) if sys.platform=="win32" \
                else subprocess.Popen(["xdg-open", pasta])
        elif ev in SCRIPTS:
            nome = ev.strip("-")
            log(win, f"\n{'─'*50}\n▶️  Executando: {nome}\n{'─'*50}")
            win["-ST-"].update(f"⏳ {nome}...")
            rodar(SCRIPTS[ev], win, nome)
        elif ev == "-TUDO-":
            log(win, "\n🚀 EXECUTANDO TUDO (Partes 2→5)...")
            for k in ["-PDF-", "-WA-", "-EMAIL-", "-XLS-"]:
                rodar(SCRIPTS[k], win, k.strip("-"))
        elif ev == "-START-":
            win["-PROG-"].update(50)
        elif ev == "-DONE-":
            nome, saida, ok = _
            log(win, saida)
            log(win, f"{'✅' if ok else '❌'} {nome} {'concluído' if ok else 'com erro'}!\n")
            win["-ST-"].update(f"{'✅' if ok else '❌'} {nome}")
            win["-PROG-"].update(0)

    win.close()

if __name__ == "__main__":
    main()

