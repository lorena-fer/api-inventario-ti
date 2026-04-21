from flask import Flask, request, jsonify

app = Flask(__name__)

items = []
current_id = 1

# -------------------------
# CORS (IMPORTANTE)
# -------------------------
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

# -------------------------
# LOGIN
# -------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Sin datos"}), 400

    if data.get("username") == "admin" and data.get("password") == "1234":
        return jsonify({"ok": True})

    return jsonify({"error": "Credenciales incorrectas"}), 401

# -------------------------
# GET ITEMS
# -------------------------
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# -------------------------
# AGREGAR ITEM
# -------------------------
@app.route('/items', methods=['POST'])
def add_item():
    global current_id
    data = request.get_json()

    nuevo = {
        "id": current_id,
        "nombre": data.get("nombre"),
        "numeroSerie": data.get("numeroSerie"),
        "descripcion": data.get("descripcion")
    }

    items.append(nuevo)
    current_id += 1

    return jsonify({"mensaje": "Agregado"})

# -------------------------
# ACTUALIZAR
# -------------------------
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()

    for i in items:
        if i["id"] == id:
            i["nombre"] = data.get("nombre")
            i["numeroSerie"] = data.get("numeroSerie")
            i["descripcion"] = data.get("descripcion")
            return jsonify({"mensaje": "Actualizado"})

    return jsonify({"error": "No encontrado"}), 404

# -------------------------
# ELIMINAR
# -------------------------
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    for i in items:
        if i["id"] == id:
            items.remove(i)
            return jsonify({"mensaje": "Eliminado"})

    return jsonify({"error": "No encontrado"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
