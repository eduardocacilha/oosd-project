from DAOs.dao import DAO
from models.evento import Evento


class EventoDAO(DAO):
    def __init__(self):
        super().__init__("eventos.pkl")

    def add(self, evento: Evento):
        if evento and isinstance(evento, Evento) and isinstance(evento.nome, str):
            super().add(evento.nome, evento)

    def update(self, evento: Evento):
        if evento and isinstance(evento, Evento) and isinstance(evento.nome, str):
            super().update(evento.nome, evento)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
