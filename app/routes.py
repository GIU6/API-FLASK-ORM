from flask import request, jsonify
from . import app, db
from .models import Cliente
from .utils import generar_codigo

# -------------------------------
# Registro
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        return jsonify({'msg': 'Faltan datos'}), 400

    # Verificar si el cliente ya existe
    if Cliente.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email ya registrado'}), 400

    # Crear cliente y guardar en DB
    cliente = Cliente(nombre=nombre, email=email, password=password)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({'msg': 'Cliente registrado'}), 201

# -------------------------------
# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente or cliente.password != password:
        return jsonify({'msg': 'Credenciales incorrectas'}), 401

    return jsonify({'msg': f'Bienvenido {cliente.nombre}'})

# -------------------------------
# Generar código
@app.route('/generar_codigo', methods=['POST'])
def generar_codigo_route():
    data = request.get_json()
    email = data.get('email')

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente:
        return jsonify({'msg': 'Cliente no encontrado'}), 404

    codigo = generar_codigo()
    cliente.codigo_verificacion = codigo
    db.session.commit()

    return jsonify({'msg': 'Código generado', 'codigo': codigo})

# -------------------------------
# Validar código
@app.route('/validar_codigo', methods=['POST'])
def validar_codigo_route():
    data = request.get_json()
    email = data.get('email')
    codigo = data.get('codigo')

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente:
        return jsonify({'msg': 'Cliente no encontrado'}), 404

    if cliente.codigo_verificacion == codigo:
        return jsonify({'msg': 'Código válido'})
    return jsonify({'msg': 'Código inválido'}), 400
