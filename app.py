from flask import Flask, render_template
import sqlitecloud

app = Flask(__name__)

DB_NAME = 'garrafas_barrio.db'
DB_QUERY = "SELECT nombre, apellido, dni, telefono, direccion FROM clientes"
CONNECTION_STRING = (
    "sqlitecloud://nmvhkjbhvk.finer-aphid.eks.use2.1kviht.sqlite.cloud:8860?apikey=KAaw2zgP5W0gi9sPpfUQ4V2ixlG7LQEja6kqTq53698"
)

@app.route('/')
def index():
    # ✅ abrir conexión POR REQUEST
    conn = sqlitecloud.connect(CONNECTION_STRING)

    conn.execute(f"USE DATABASE {DB_NAME}")

    cursor = conn.execute(DB_QUERY)
    rows = cursor.fetchall()   # 🔥 CLAVE

    conn.close()               # ahora sí, seguro cerrar

    clientes = []
    for row in rows:
        clientes.append({
            "nombre": row[0],
            "apellido": row[1],
            "dni": row[2],
            "telefono": row[3],
            "direccion": row[4]
        })

    return render_template("index.html", clientes=clientes)

if __name__ == '__main__':
    app.run(debug=True)






