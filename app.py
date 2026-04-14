from flask import Flask, request, jsonify

app = Flask(__name__)

devices = []
current_id = 1

@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devices)

@app.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    for d in devices:
        if d['id'] == id:
            return jsonify(d)
    return jsonify({"error": "No encontrado"}), 404

@app.route('/devices', methods=['POST'])
def create_device():
    global current_id
    data = request.json

    if not data:
        return jsonify({"error": "Datos vacíos"}), 400

    device = {
        "id": current_id,
        "nombre": data.get("nombre", ""),
        "tipo": data.get("tipo", ""),
        "estado": data.get("estado", ""),
        "area": data.get("area", ""),
        "fecha_registro": data.get("fecha_registro", "")
    }

    devices.append(device)
    current_id += 1

    return jsonify(device), 201

@app.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    data = request.json
    for d in devices:
        if d['id'] == id:
            d.update(data)
            return jsonify(d)
    return jsonify({"error": "No encontrado"}), 404

@app.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    for d in devices:
        if d['id'] == id:
            devices.remove(d)
            return jsonify({"mensaje": "Eliminado"})
    return jsonify({"error": "No encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)