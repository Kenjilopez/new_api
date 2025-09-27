from flask import Flask
from controllers.car_controller import car_store_bp  # ← Corrección aquí

app = Flask(__name__)

# Registrar el blueprint de tiendas de carros
app.register_blueprint(car_store_bp)

if __name__ == "__main__":
    app.run(debug=True)
