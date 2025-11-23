from DAOs.dao import DAO
from models.feedback import Feedback


class FeedbackDAO(DAO):

    def __init__(self):
        super().__init__("feedbacks.pkl")

    @staticmethod
    def _make_key(feedback: Feedback) -> str:
        return f"{feedback.usuario.matricula}:{feedback.evento.nome}".lower()

    @staticmethod
    def make_key(matricula: str, nome_evento: str) -> str:
        if not isinstance(matricula, str) or not isinstance(nome_evento, str):
            return ""
        return f"{matricula}:{nome_evento}".lower()

    def add(self, feedback: Feedback):
        if (
            feedback
            and isinstance(feedback, Feedback)
            and hasattr(feedback.usuario, "matricula")
            and isinstance(feedback.usuario.matricula, str)
            and hasattr(feedback.evento, "nome")
            and isinstance(feedback.evento.nome, str)
        ):
            super().add(self._make_key(feedback), feedback)

    def update(self, feedback: Feedback):
        if (
            feedback
            and isinstance(feedback, Feedback)
            and hasattr(feedback.usuario, "matricula")
            and isinstance(feedback.usuario.matricula, str)
            and hasattr(feedback.evento, "nome")
            and isinstance(feedback.evento.nome, str)
        ):
            super().update(self._make_key(feedback), feedback)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key.lower())

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key.lower())

    def get_por_usuario_evento(self, matricula: str, nome_evento: str):
        key = self.make_key(matricula, nome_evento)
        if key:
            return super().get(key)

    def remove_por_usuario_evento(self, matricula: str, nome_evento: str):
        key = self.make_key(matricula, nome_evento)
        if key:
            return super().remove(key)
