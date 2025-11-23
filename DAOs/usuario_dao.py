from DAOs.dao import DAO
from models.usuario import Usuario


class UsuarioDAO(DAO):

    def __init__(self):
        super().__init__("usuarios.pkl")

    def add(self, usuario: Usuario):
        if (
            usuario is not None
            and isinstance(usuario, Usuario)
            and isinstance(usuario.matricula, str)
        ):
            super().add(usuario.matricula, usuario)

    def update(self, usuario: Usuario):
        if (
            usuario is not None
            and isinstance(usuario, Usuario)
            and isinstance(usuario.matricula, str)
        ):
            super().update(usuario.matricula, usuario)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
