# Configuración de JWT
import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","clave_super_segura")
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"