from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.user_repository import User, Base

user_bp = Blueprint('user', __name__)

engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'Faltan datos'}), 400

    session = Session()
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.close()
    return jsonify({'message': 'Usuario creado'}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    session = Session()
    users = session.query(User).all()
    result = [
        {'id': user.id, 'name': user.name, 'email': user.email}
        for user in users
    ]
    session.close()
    return jsonify(result), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    session = Session()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return jsonify({'error': 'Usuario no encontrado'}), 404
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    session.commit()
    session.close()
    return jsonify({'message': 'Usuario actualizado'}), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return jsonify({'error': 'Usuario no encontrado'}), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify({'message': 'Usuario eliminado'}), 200