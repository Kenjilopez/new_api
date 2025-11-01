from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.car_repository import Car, CarStore, Base

car_store_bp = Blueprint('car_store', __name__)

# Configura la conexión a la base de datos (ajusta la ruta si es necesario)
engine = create_engine('sqlite:///cars.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def admin_required():
    # identity is the subject (string id). Read additional claims with get_jwt()
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Acceso denegado: solo administradores'}), 403
 
 
@car_store_bp.route('/cars', methods=['POST'])
@jwt_required()
def add_car():
    data = request.get_json()
    model = data.get('model')
    store_id = data.get('store_id')
    if not model or not store_id:
        return jsonify({'error': 'Faltan datos'}), 400

    session = Session()
    car = Car(model=model, store_id=store_id)
    session.add(car)
    session.commit()
    session.close()
    return jsonify({'message': 'Carro insertado correctamente'}), 201

@car_store_bp.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    session = Session()
    cars = session.query(Car).all()
    result = [
        {'id': car.id, 'model': car.model, 'store_id': car.store_id}
        for car in cars
    ]
    session.close()
    return jsonify(result), 200

@car_store_bp.route('/cars/<int:car_id>', methods=['PUT'])
@jwt_required()    
def update_car(car_id):
    car = session.query(Car).get(car_id)
    if not car:
        session.close()
        return jsonify({'error': 'Carro no encontrado'}), 404
    car.model = data.get('model', car.model)
    car.store_id = data.get('store_id', car.store_id)
    session.commit()
    session.close()
    return jsonify({'message': 'Carro actualizado'}), 200

@car_store_bp.route('/cars/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    session = Session()
    car = session.query(Car).get(car_id)
    if not car:
        session.close()
        return jsonify({'error': 'Carro no encontrado'}), 404
    session.delete(car)
    session.commit()
    session.close()
    return jsonify({'message': 'Carro eliminado'}), 200