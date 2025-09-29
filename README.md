Install these packages:(👇)

pip install -r requirements.txt


Para Correr el programa usar
python main.py

Para correr las Instrucciones CRUD of Cars

POST  ----Crear----
http://127.0.0.1:5000/cars/{id}
{
  "model": "Nissan",
  "store_id": "Gasolina"
}

DELETE ---Eliminar un registro---
http://127.0.0.1:5000/cars/{id}

PUT ----Actualizar---
http://127.0.0.1:5000/cars/{id}
{
  "model": "Nissan",
  "store_id": "Gasolina"
}

GET --Obtener----
http://127.0.0.1:5000/cars/{id}


Para correr las Instrucciones CRUD of users

http://127.0.0.1:5000/registry

In the raw insert this:(👇)

{
  "username": "your_username",
  "password": "your_password"
}

http://127.0.0.1:5000/login

In the raw insert this:(👇), later in the body show your access_token

{
  "username": "your_username",
  "password": "your_password"
}
