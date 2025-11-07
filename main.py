from flask import Flask, send_from_directory, render_template
from config.jwt import *
from controllers.car_controller import car_store_bp
from controllers.user_controller import user_bp, register_jwt_error_handlers
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# Configurar JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
app.config['JWT_HEADER_NAME'] = JWT_HEADER_NAME
app.config['JWT_HEADER_TYPE'] = JWT_HEADER_TYPE

jwt = JWTManager(app)

# Registrar los blueprints
app.register_blueprint(car_store_bp)
app.register_blueprint(user_bp)


# Registrar manejadores personalizados de error JWT
register_jwt_error_handlers(app)

# Ruta para servir el frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)