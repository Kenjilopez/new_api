from flask import Flask
from controllers.car_controller import car_store_bp
from controllers.user_controller import user_bp

app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(car_store_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)