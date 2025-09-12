from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos simulados: carros con marca y tipo de energía
carros = [
    {"id": 1, "marca": "Toyota", "combustible": "Gasolina"},
    {"id": 2, "marca": "Tesla", "combustible": "Eléctrica"},
    {"id": 3, "marca": "nissan", "combustible": "Diesel"},
    {"id": 4, "marca": "Chevrolet", "combustible": "Gasolina"},
    {"id": 5, "marca": "BYD", "combustible": "Eléctrica"}
]

# Obtener todos los carros
@app.route('/carros', methods=['GET'])
def get_carros():
    return jsonify(carros), 200

# Obtener un carro por ID
@app.route('/carros/<int:carro_id>', methods=['GET'])
def get_carro(carro_id):
    carro = next((c for c in carros if c['id'] == carro_id), None)
    if carro is None:
        return jsonify({'error': 'Carro no encontrado'}), 404
    return jsonify(carro), 200

# Crear un nuevo carro
@app.route('/carros', methods=['POST'])
def create_carro():
    if not request.json or 'marca' not in request.json or 'lena' not in request.json:
        return jsonify({'error': 'Solicitud incorrecta'}), 400
    new_id = max(c['id'] for c in carros) + 1 if carros else 1
    carro = {
        'id': new_id,
        'marca': request.json['marca'],
        'lena': request.json['lena']
    }
    carros.append(carro)
    return jsonify(carro), 201

# Actualizar un carro existente
@app.route('/carros/<int:carro_id>', methods=['PUT'])
def update_carro(carro_id):
    carro = next((c for c in carros if c['id'] == carro_id), None)
    if carro is None:
        return jsonify({'error': 'Carro no encontrado'}), 404
    if not request.json:
        return jsonify({'error': 'Solicitud incorrecta'}), 400
    carro['marca'] = request.json.get('marca', carro['marca'])
    carro['lena'] = request.json.get('lena', carro['lena'])
    return jsonify(carro), 200

# Eliminar un carro
@app.route('/carros/<int:carro_id>', methods=['DELETE'])
def delete_carro(carro_id):
    carro = next((c for c in carros if c['id'] == carro_id), None)
    if carro is None:
        return jsonify({'error': 'Carro no encontrado'}), 404
    carros.remove(carro)
    return jsonify({'resultado': 'Carro eliminado'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
