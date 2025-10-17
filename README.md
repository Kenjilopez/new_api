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

http://127.0.0.1:5000/registry [POST]

In the raw insert this:(👇)

{
  "email": "your_email",
  "password": "your_password"
}

http://127.0.0.1:5000/login [POST]

In the raw insert this:(👇), later in the body show your access_token

{
  "email": "your_email",
  "password": "your_password"
}

http://127.0.0.1:5000/refresh [POST]

Autorization 
Auth type:  Bearer Token 

Token: "your refresh token given u when u making login" ❗

Warming: you have only 1 minute for use this token ⚠

http://127.0.0.1:5000/users  [GET]

Autorization 
Auth type:  Bearer Token 

Token: "your refresh token given u when u making login" ❗

http://127.0.0.1:5000/users/id [PUT]
To modify
{
    "email": "ejemplo@hotmail.com",
    "password": "ejemplo"
}

http://127.0.0.1:5000/users/id [DELETE]

Autorization 
Auth type:  Bearer Token 

Token: "your refresh token given u when u making login" ❗

Warming: You can delete an user if you user had as Role "admin"  ⚠

