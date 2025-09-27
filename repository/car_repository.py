# Importaciones de librerías:
# - sqlalchemy: Proporciona herramientas para trabajar con bases de datos relacionales en Python mediante ORM (Object Relational Mapping).
#   - Column, Integer, String, ForeignKey: Permiten definir los tipos de columnas y relaciones entre tablas en los modelos de base de datos.
# - sqlalchemy.orm: Incluye utilidades para la gestión de relaciones y la declaración de modelos.
#   - relationship: Permite definir relaciones entre tablas (por ejemplo, uno a muchos).
#   - declarative_base: Se utiliza para crear una clase base a partir de la cual se definen los modelos ORM.

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Session

Base = declarative_base()


"""
La clase CarStore representa una tienda de carros dentro del sistema. Cada instancia de esta clase corresponde a una tienda específica,
almacenando información relevante como su nombre y la relación con sus carros. Esta clase está mapeada a la tabla 'car_stores' en
la base de datos y permite gestionar la información de las tiendas, así como acceder a todos los carros asociados a cada tienda
mediante una relación uno a muchos.
"""
class CarStore(Base):
    __tablename__ = 'car_stores'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cars = relationship('Car', back_populates='store', cascade='all, delete-orphan')


"""
La clase Car representa un carro que pertenece a una tienda de carros. Cada instancia de esta clase corresponde a un carro específico,
almacenando información como el modelo y la referencia a la tienda a la que pertenece. Esta clase está mapeada a la tabla 'cars' en
la base de datos y permite gestionar los carros, así como establecer la relación de pertenencia con una tienda mediante una clave foránea.
"""
class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(255), nullable=False)
    store_id = Column(Integer, ForeignKey('car_stores.id'))
    store = relationship('CarStore', back_populates='cars')


# Funciones CRUD para el repositorio de carros

def get_all_cars(session: Session):
    return session.query(Car).all()


def get_car_by_id(session: Session, car_id: int):
    return session.query(Car).get(car_id)


def create_car(session: Session, model: str, store_id: int):
    car = Car(model=model, store_id=store_id)
    session.add(car)
    session.commit()
    return car


def update_car(session: Session, car_id: int, model: str = None, store_id: int = None):
    car = session.query(Car).get(car_id)
    if not car:
        return None
    if model:
        car.model = model
    if store_id:
        car.store_id = store_id
    session.commit()
    return car


def delete_car(session: Session, car_id: int):
    car = session.query(Car).get(car_id)
    if not car:
        return False
    session.delete(car)
    session.commit()
    return True

# Dentro de tus rutas Flask, crea una sesión y llama a estas funciones.