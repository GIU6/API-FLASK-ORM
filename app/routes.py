from flask import request, jsonify
from . import app, db
from .models import Cliente
import random


def generar_codigo():
    return str(random.randint(1000, 9999))


@app.route('/')
def index():
    return "API REST /register, /login, /generar_codigo, /validar_codigo"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if Cliente.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email ya registrado'}), 400

    cliente = Cliente(nombre=nombre, email=email, password=password)
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'msg': 'Cliente registrado'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente or cliente.password != password:
        return jsonify({'msg': 'Credenciales incorrectas'}), 401
    return jsonify({'msg': f'Bienvenido {cliente.nombre}'})


@app.route('/generar_codigo', methods=['POST'])
def codigo():
    data = request.get_json()
    email = data.get('email')

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente:
        return jsonify({'msg': 'Cliente no encontrado'}), 404

    cliente.codigo = generar_codigo()
    db.session.commit()
    return jsonify({'msg': 'Código generado', 'codigo': cliente.codigo})


@app.route('/validar_codigo', methods=['POST'])
def validar():
    data = request.get_json()
    email = data.get('email')
    codigo = data.get('codigo')

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente:
        return jsonify({'msg': 'Cliente no encontrado'}), 404

    if cliente.codigo == codigo:
        return jsonify({'msg': 'Código válido'})
    return jsonify({'msg': 'Código inválido'}), 400
