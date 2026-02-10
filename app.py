from flask import Flask, render_template, request, redirect, jsonify
import sqlitecloud

app = Flask(__name__)

DB_NAME = "garrafas_barrio.db"
CONNECTION_STRING = (
    "sqlitecloud://nmvhkjbhvk.finer-aphid.eks.use2.1kviht.sqlite.cloud:8860"
    "?apikey=KAaw2zgP5W0gi9sPpfUQ4V2ixlG7LQEja6kqTq53698"
)
# =========================
# MOSTRAR CLIENTES (JSON)
# =========================
@app.route("/clientes")
def clientes():
    clientes = obtener_clientes()
    return jsonify(clientes)



# =========================
# CONEXIÓN REUTILIZABLE
# =========================
def get_connection():
    conn = sqlitecloud.connect(CONNECTION_STRING)
    conn.execute(f"USE DATABASE {DB_NAME}")
    return conn


# =========================
# TRAER CLIENTES
# =========================
def obtener_clientes():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT nombre, apellido, dni, telefono, direccion
        FROM clientes
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    clientes = []
    for r in rows:
        clientes.append({
            "nombre": r[0],
            "apellido": r[1],
            "dni": r[2],
            "telefono": r[3],
            "direccion": r[4],
        })

    return clientes


# =========================
# HOME / LISTADO
# =========================
@app.route("/")
def index():
    clientes = obtener_clientes()
    return render_template("index.html", clientes=clientes)


# =========================
# AGREGAR CLIENTE (FORM)
# =========================
@app.route("/agregar_cliente", methods=["POST"])
def agregar_cliente():
    nombre = request.form["cliente-nombre"]
    apellido = request.form["cliente-apellido"]
    dni = request.form["cliente-dni"]
    telefono = request.form["cliente-telefono"]
    direccion = request.form["cliente-direccion"]

    conn = get_connection()

    conn.execute("""
        INSERT INTO clientes (
            nombre, apellido, dni, telefono, direccion
        )
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, apellido, dni, telefono, direccion))

    conn.close()

    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)









