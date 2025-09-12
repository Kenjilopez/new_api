Para Correr el programa usar
python .\models\app.py

Para correr las Instrucciones CRUD  usar Postman

POST  ----Crear----
http://127.0.0.1:5000/carros/{id}
{
  "marca": "Nissan",
  "lena": "Gasolina"
}

DELETE ---Eliminar un registro---
http://127.0.0.1:5000/carros/{id}

PUT ----Actualizar---
http://127.0.0.1:5000/carros/{id}
{
  "marca": "Nissan",
  "lena": "Gasolina"
}

GET --Obtener----
http://127.0.0.1:5000/carros/{id}

