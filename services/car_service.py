from repository.car_repository import (
	get_all_cars,
	get_car_by_id,
	create_car,
	update_car,
	delete_car
)
from models.car_model import Base
from sqlalchemy.orm import Session

"""
Librerías utilizadas:
- repository.car_repository: Proporciona funciones para la gestión de carros en la base de datos.
- models.car_model: Define el modelo Car que representa la entidad de carro.
- sqlalchemy.orm.Session: Permite manejar la sesión de la base de datos para realizar operaciones transaccionales.
"""

class CarService:
	"""
	Capa de servicios para la gestión de carros.
	Esta clase orquesta la lógica de negocio relacionada con los carros, utilizando el repositorio para acceder a los datos.
	Permite mantener la lógica de negocio separada de la capa de acceso a datos y de la base de datos.
	"""
	def __init__(self, db_session: Session):
		"""
		Inicializa el servicio de carros con una sesión de base de datos.
		"""
		self.db_session = db_session

	def listar_carros(self):
		"""
		Recupera y retorna todos los carros registrados en el sistema.
		Utiliza el repositorio para obtener la lista completa de carros.
		"""
		return get_all_cars(self.db_session)

	def obtener_carro(self, car_id: int):
		"""
		Busca y retorna un carro específico por su identificador único (ID).
		Utiliza el repositorio para acceder al carro correspondiente.
		"""
		return get_car_by_id(self.db_session, car_id)

	def crear_carro(self, model: str, store_id: int):
		"""
		Crea un nuevo carro con el modelo y tienda proporcionados.
		Utiliza el repositorio para almacenar el nuevo carro en la base de datos.
		"""
		return create_car(self.db_session, model, store_id)

	def actualizar_carro(self, car_id: int, model: str = None, store_id: int = None):
		"""
		Actualiza la información de un carro existente, permitiendo modificar su modelo y tienda.
		Utiliza el repositorio para realizar la actualización en la base de datos.
		"""
		return update_car(self.db_session, car_id, model, store_id)

	def eliminar_carro(self, car_id: int):
		"""
		Elimina un carro del sistema según su identificador único (ID).
		Utiliza el repositorio para eliminar el carro de la base de datos.
		"""
		return delete_car(self.db_session, car_id)
