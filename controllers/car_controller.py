from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.car_repository import Car, CarStore, Base
from controllers.auth_controller import token_required, admin_required

car_store_bp = Blueprint('car_store', __name__)

# Configure database connection
engine = create_engine('sqlite:///cars.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
 
 
@car_store_bp.route('/cars', methods=['POST'])
@admin_required
def add_car(current_user):
    try:
        data = request.get_json()
        model = data.get('model')
        store_id = data.get('store_id')
        if not model or not store_id:
            return jsonify({'error': 'Missing data'}), 400

        try:
            store_id = int(store_id)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid store ID'}), 400

        session = Session()
        car = Car(model=model, store_id=store_id)
        session.add(car)
        session.commit()
        session.close()
        return jsonify({'message': 'Car added successfully'}), 201
    except Exception as e:
        if 'session' in locals():
            session.rollback()
            session.close()
        return jsonify({'error': str(e)}), 500

@car_store_bp.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user):
    session = Session()
    cars = session.query(Car).all()
    result = [
        {'id': car.id, 'model': car.model, 'store_id': car.store_id}
        for car in cars
    ]
    session.close()
    return jsonify(result), 200

@car_store_bp.route('/cars/<int:car_id>', methods=['PUT'])
@admin_required
def update_car(current_user, car_id):
    session = None
    try:
        session = Session()
        car = session.query(Car).get(car_id)
        if not car:
            session.close()
            return jsonify({'error': 'Car not found'}), 404
        
        data = request.get_json()
        car.model = data.get('model', car.model)
        
        store_id = data.get('store_id')
        if store_id is not None:
            try:
                car.store_id = int(store_id)
            except (ValueError, TypeError):
                session.close()
                return jsonify({'error': 'Invalid store ID'}), 400
                
        session.commit()
        session.close()
        return jsonify({'message': 'Car updated successfully'}), 200
    except Exception as e:
        if session:
            session.rollback()
            session.close()
        return jsonify({'error': str(e)}), 500

@car_store_bp.route('/cars/<int:car_id>', methods=['DELETE'])
@admin_required
def delete_car(current_user, car_id):
    session = Session()
    car = session.query(Car).get(car_id)
    if not car:
        session.close()
        return jsonify({'error': 'Car not found'}), 404
    session.delete(car)
    session.commit()
    session.close()
    return jsonify({'message': 'Car deleted successfully'}), 200