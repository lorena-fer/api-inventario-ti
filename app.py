from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔥 BASE DE DATOS REAL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 🔥 CORS (para que funcione con HTML / GitHub)
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

# 🔥 MODELO
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    numeroSerie = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))

# 🔥 CREAR BD
with app.app_context():
    db.create_all()

# 🔐 LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if data.get("username") == "admin" and data.get("password") == "1234":
        return jsonify({"ok": True})

    return jsonify({"error": "Credenciales incorrectas"}), 401

# 📥 OBTENER
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([
        {
            "id": i.id,
            "nombre": i.nombre,
            "numeroSerie": i.numeroSerie,
            "descripcion": i.descripcion
        } for i in items
    ])

# ➕ AGREGAR
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()

    nuevo = Item(
        nombre=data.get('nombre'),
        numeroSerie=data.get('numeroSerie'),
        descripcion=data.get('descripcion')
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"mensaje": "Agregado"})

# ✏️ ACTUALIZAR
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = Item.query.get(id)

    if not item:
        return jsonify({"error": "No encontrado"}), 404

    item.nombre = data.get('nombre')
    item.numeroSerie = data.get('numeroSerie')
    item.descripcion = data.get('descripcion')

    db.session.commit()

    return jsonify({"mensaje": "Actualizado"})

# ❌ ELIMINAR
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)

    if not item:
        return jsonify({"error": "No encontrado"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"mensaje": "Eliminado"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
