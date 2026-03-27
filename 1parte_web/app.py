from flask import Flask, render_template, request, redirect, url_for, flash
from database import criar_tabelas, conectar

app = Flask(__name__)
app.secret_key = "techsolutions2025"

criar_tabelas()

# ─── DASHBOARD ────────────────────────────────────────────────
@app.route("/")
def index():
    conn = conectar()
    cur  = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM faturas")
    total_faturas = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM faturas WHERE status = 'pendente'")
    faturas_pendentes = cur.fetchone()[0]
    conn.close()
    return render_template("index.html",
                           total_clientes=total_clientes,
                           total_faturas=total_faturas,
                           faturas_pendentes=faturas_pendentes)

# ─── CLIENTES ─────────────────────────────────────────────────
@app.route("/clientes")
def listar_clientes():
    conn = conectar()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM clientes ORDER BY nome")
    clientes = cur.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if request.method == "POST":
        nome     = request.form["nome"].strip()
        email    = request.form["email"].strip()
        telefone = request.form["telefone"].strip()
        endereco = request.form.get("endereco", "").strip()

        if not nome or not email or not telefone:
            flash("Preencha todos os campos obrigatórios.", "erro")
            return render_template("form_cliente.html")

        conn = conectar()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?)",
            (nome, email, telefone, endereco)
        )
        conn.commit()
        conn.close()
        flash(f"Cliente '{nome}' cadastrado com sucesso!", "sucesso")
        return redirect(url_for("listar_clientes"))

    return render_template("form_cliente.html")

@app.route("/clientes/excluir/<int:id>")
def excluir_cliente(id):
    conn = conectar()
    cur  = conn.cursor()
    cur.execute("DELETE FROM faturas WHERE cliente_id = ?", (id,))
    cur.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Cliente excluído.", "info")
    return redirect(url_for("listar_clientes"))

# ─── FATURAS ──────────────────────────────────────────────────
@app.route("/faturas")
def listar_faturas():
    conn = conectar()
    cur  = conn.cursor()
    cur.execute("""
        SELECT f.id, c.nome, c.email, c.telefone,
               f.valor, f.data_vencimento, f.status, f.data_emissao
        FROM faturas f
        JOIN clientes c ON f.cliente_id = c.id
        ORDER BY f.data_vencimento
    """)
    faturas = cur.fetchall()
    conn.close()
    return render_template("faturas.html", faturas=faturas)

@app.route("/faturas/nova", methods=["GET", "POST"])
def nova_fatura():
    conn = conectar()
    cur  = conn.cursor()

    if request.method == "POST":
        cliente_id      = request.form["cliente_id"]
        valor           = request.form["valor"]
        data_vencimento = request.form["data_vencimento"]

        if not cliente_id or not valor or not data_vencimento:
            flash("Preencha todos os campos.", "erro")
            cur.execute("SELECT id, nome FROM clientes ORDER BY nome")
            clientes = cur.fetchall()
            conn.close()
            return render_template("form_fatura.html", clientes=clientes)

        cur.execute(
            "INSERT INTO faturas (cliente_id, valor, data_vencimento) VALUES (?, ?, ?)",
            (cliente_id, float(valor), data_vencimento)
        )
        conn.commit()
        conn.close()
        flash("Fatura emitida com sucesso!", "sucesso")
        return redirect(url_for("listar_faturas"))

    cur.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cur.fetchall()
    conn.close()
    return render_template("form_fatura.html", clientes=clientes)

# ─── START ────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)