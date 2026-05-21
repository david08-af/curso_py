from flask import Flask, render_template_string, request, jsonify, session, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_desarrollo'
DB_NAME = 'gestion_pacientes.db'

def conectar_db():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion

# Crear las tablas al arrancar si no existen
conn = conectar_db()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        correo TEXT UNIQUE,
        contrasena TEXT,
        fecha_registro TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        nombre TEXT,
        monto_a_pagar REAL DEFAULT 0.0,
        estado_pago TEXT DEFAULT 'Pendiente',
        ultima_actualizacion TEXT
    )
''')
conn.commit()
conn.close()

# ---- DISEÑOS HTML (Todo metido acá adentro para no usar carpetas) ----
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ingreso al Sistema</title>
    <style>
        body { font-family: sans-serif; background: #f4f6f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 350px; }
        h2 { text-align: center; color: #1e3a8a; margin-bottom: 20px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #1e3a8a; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button.register { background: #10b981; }
        .error { color: red; font-size: 13px; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Gestión Médica</h2>
        <input type="email" id="correo" placeholder="Correo electrónico" required>
        <input type="password" id="contrasena" placeholder="Contraseña" required>
        <button onclick="enviar('login')">Iniciar Sesión</button>
        <button class="register" onclick="enviar('registrar')">Registrarse</button>
        <div id="mensaje" class="error"></div>
    </div>
    <script>
        async function enviar(accion) {
            const correo = document.getElementById('correo').value;
            const contrasena = document.getElementById('contrasena').value;
            if(!correo || !contrasena) return alert('Completá los campos');
            const res = await fetch(`/api/${accion}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({correo, contrasena})
            });
            const data = await res.json();
            if(res.ok) {
                if(accion === 'login') window.location.reload();
                else alert('Registrado con éxito. Ya podés iniciar sesión.');
            } else {
                document.getElementById('mensaje').innerText = data.message || "Error";
            }
        }
    </script>
</body>
</html>
'''

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Planilla de Pacientes</title>
    <style>
        * { box-sizing: border-box; font-family: sans-serif; margin: 0; padding: 0; }
        body { background-color: #f4f6f9; padding: 20px; }
        .header { display: flex; justify-content: space-between; background: white; padding: 15px 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }
        h1 { color: #1e3a8a; font-size: 22px; }
        .controls { display: flex; gap: 15px; margin-bottom: 20px; }
        input[type="text"] { padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; width: 250px; }
        button { background-color: #10b981; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .logout-btn { background-color: #ef4444; text-decoration: none; color: white; padding: 8px 16px; border-radius: 6px; font-weight: bold; font-size: 14px;}
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        th { background-color: #1e3a8a; color: white; padding: 12px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
        .input-table { width: 100%; border: none; background: transparent; font-size: 14px; }
        .input-table:focus { outline: 2px solid #3b82f6; background: white; }
        .total { text-align: right; margin-top: 20px; font-size: 18px; font-weight: bold; color: #1e3a8a; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Planilla de Cobros</h1>
        <a class="logout-btn" href="/logout">Cerrar Sesión</a>
    </div>
    <div class="controls">
        <input type="text" id="buscador" placeholder="🔍 Buscar paciente..." onkeyup="filtrar()">
        <button onclick="agregarFila()">＋ Agregar Paciente</button>
    </div>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">ID</th>
                <th style="width: 50%;">Nombre del Paciente</th>
                <th style="width: 20%;">Monto ($)</th>
                <th style="width: 20%;">Estado</th>
            </tr>
        </thead>
        <tbody id="tabla-cuerpo"></tbody>
    </table>
    <div class="total">Total Pendiente: <span id="total-general" style="color:#10b981;">$ 0.00</span></div>
    <script>
        let pacientes = [];
        async function cargarTabla() {
            const res = await fetch('/api/pacientes');
            pacientes = await res.json();
            const cuerpo = document.getElementById("tabla-cuerpo");
            cuerpo.innerHTML = "";
            pacientes.forEach(p => {
                const fila = document.createElement("tr");
                fila.className = "fila";
                fila.innerHTML = `
                    <td>${p.id}</td>
                    <td><input type="text" class="input-table" value="${p.nombre}" onchange="guardar(${p.id}, 'nombre', this.value)"></td>
                    <td><input type="number" class="input-table" value="${p.monto_a_pagar}" onchange="guardar(${p.id}, 'monto_a_pagar', this.value)"></td>
                    <td>
                        <select class="input-table" onchange="guardar(${p.id}, 'estado_pago', this.value)">
                            <option value="Pendiente" ${p.estado_pago === 'Pendiente' ? 'selected' : ''}>⏳ Pendiente</option>
                            <option value="Pagado" ${p.estado_pago === 'Pagado' ? 'selected' : ''}>✅ Pagado</option>
                        </select>
                    </td>
                `;
                cuerpo.appendChild(fila);
            });
            calcular();
        }
        async function agregarFila() {
            await fetch('/api/pacientes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({nombre: "Nuevo Paciente", monto_a_pagar: 0, estado_pago: "Pendiente"})
            });
            cargarTabla();
        }
        async function guardar(id, campo, valor) {
            const p = pacientes.find(x => x.id === id);
            if (p) {
                p[campo] = campo === 'monto_a_pagar' ? parseFloat(valor) || 0 : valor;
                await fetch('/api/pacientes', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(p)
                });
            }
            calcular();
        }
        function calcular() {
            const total = pacientes.filter(p => p.estado_pago === "Pendiente").reduce((s, p) => s + p.monto_a_pagar, 0);
            document.getElementById("total-general").innerText = `$ ${total.toFixed(2)}`;
        }
        function filtrar() {
            const f = document.getElementById("buscador").value.toLowerCase();
            document.querySelectorAll(".fila").forEach(fila => {
                const n = fila.querySelectorAll("input")[0].value.toLowerCase();
                fila.style.display = n.includes(f) ? "" : "none";
            });
        }
        window.onload = cargarTabla;
    </script>
</body>
</html>
'''

# ---- RUTAS ----
@app.route('/')
def inicio():
    if 'usuario_id' in session:
        return render_template_string(INDEX_HTML, correo=session['correo'])
    return render_template_string(LOGIN_HTML)

@app.route('/api/registrar', methods=['POST'])
def registrar():
    datos = request.json
    correo = datos.get('correo')
    contrasena = datos.get('contrasena')
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (correo, contrasena, fecha_registro) VALUES (?, ?, ?)',
                       (correo, contrasena, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "El correo ya existe"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    datos = request.json
    correo = datos.get('correo')
    contrasena = datos.get('contrasena')
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE correo = ? AND contrasena = ?', (correo, contrasena))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        session['usuario_id'] = usuario['id']
        session['correo'] = usuario['correo']
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Datos incorrectos"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/pacientes', methods=['GET'])
def obtener_pacientes():
    if 'usuario_id' not in session: return jsonify([]), 401
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE usuario_id = ?', (session['usuario_id'],))
    pacientes = [dict(fila) for fila in cursor.fetchall()]
    conn.close()
    return jsonify(pacientes)

@app.route('/api/pacientes', methods=['POST'])
def guardar_paciente():
    if 'usuario_id' not in session: return jsonify({"error": "No autorizado"}), 401
    datos = request.json
    conn = conectar_db()
    cursor = conn.cursor()
    id_p = datos.get('id')
    nombre = datos.get('nombre', '')
    monto = datos.get('monto_a_pagar', 0)
    estado = datos.get('estado_pago', 'Pendiente')
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if id_p:
        cursor.execute('UPDATE pacientes SET nombre=?, monto_a_pagar=?, estado_pago=?, ultima_actualizacion=? WHERE id=? AND usuario_id=?',
                       (nombre, monto, estado, ahora, id_p, session['usuario_id']))
    else:
        cursor.execute('INSERT INTO pacientes (usuario_id, nombre, monto_a_pagar, estado_pago, ultima_actualizacion) VALUES (?,?,?,?,?)',
                       (session['usuario_id'], nombre, monto, estado, ahora))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)