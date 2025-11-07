from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user_model import User
from repository.car_repository import Base
import jwt
from datetime import datetime, timedelta
from functools import wraps
from config.jwt import JWT_SECRET_KEY
from flask import current_app

auth_bp = Blueprint('auth', __name__)

# Database setup
engine = create_engine('sqlite:///cars.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def create_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            session = Session()
            current_user = session.query(User).filter_by(id=data['user_id']).first()
            session.close()
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
            return f(current_user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            if data['role'] != 'admin':
                return jsonify({'error': 'Admin privileges required'}), 403
            
            session = Session()
            current_user = session.query(User).filter_by(id=data['user_id']).first()
            session.close()
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
            return f(current_user, *args, **kwargs)
        except:
            return jsonify({'error': 'Invalid token'}), 401

    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'client')  # default to client if not specified

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    if role not in ['admin', 'client']:
        return jsonify({'error': 'Invalid role'}), 400

    session = Session()
    if session.query(User).filter_by(username=username).first():
        session.close()
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username, role=role)
    user.set_password(password)
    
    session.add(user)
    session.commit()
    
    # Create token
    token = create_token(user.id, user.role)
    
    session.close()
    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    session = Session()
    user = session.query(User).filter_by(username=username).first()
    
    if user and user.check_password(password):
        token = create_token(user.id, user.role)
        session.close()
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
    
    session.close()
    return jsonify({'error': 'Invalid username or password'}), 401