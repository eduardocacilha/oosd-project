import unittest
from controllers.main_controller import MainController

class TestSistemaFestas(unittest.TestCase):
    def setUp(self):
        self.controller = MainController()

    def test_adicionar_usuario(self):
        self.controller.adicionar_usuario("123", "Alice", "alice@email.com")
        self.assertEqual(len(self.controller.usuarios), 1)
        self.assertEqual(self.controller.usuarios[0].nome, "Alice")

    def test_alterar_usuario(self):
        self.controller.adicionar_usuario("123", "Alice", "alice@email.com")
        usuario = self.controller.usuarios[0]
        usuario.nome = "Alicia"
        usuario.email = "alicia@email.com"
        self.assertEqual(usuario.nome, "Alicia")
        self.assertEqual(usuario.email, "alicia@email.com")

    def test_excluir_usuario(self):
        self.controller.adicionar_usuario("123", "Alice", "alice@email.com")
        usuario = self.controller.usuarios[0]
        self.controller.usuarios.remove(usuario)
        self.assertEqual(len(self.controller.usuarios), 0)

    def test_adicionar_evento(self):
        from models.evento import Evento
        evento = Evento("Festa", "2024-10-10", "Salão", 50.0)
        self.controller.adicionar_evento(evento)
        self.assertEqual(len(self.controller.eventos), 1)
        self.assertEqual(self.controller.eventos[0].nome, "Festa")

    def test_comprar_ingresso(self):
        from models.evento import Evento
        self.controller.adicionar_usuario("123", "Alice", "alice@email.com")
        evento = Evento("Festa", "2024-10-10", "Salão", 50.0)
        self.controller.adicionar_evento(evento)
        usuario = self.controller.usuarios[0]
        self.controller.comprar_ingresso(usuario, evento)
        self.assertEqual(len(self.controller.ingressos), 1)

    def test_listar_ingressos_usuario(self):
        from models.evento import Evento
        self.controller.adicionar_usuario("123", "Alice", "alice@email.com")
        evento = Evento("Festa", "2024-10-10", "Salão", 50.0)
        self.controller.adicionar_evento(evento)
        usuario = self.controller.usuarios[0]
        self.controller.comprar_ingresso(usuario, evento)
        ingressos = usuario.listar_ingressos()
        self.assertEqual(len(ingressos), 1)

    def test_avaliar_evento(self):
        from models.evento import Evento
        self.controller.adicionar_usuario("123", "Alice", "alice@email.com")
        evento = Evento("Festa", "2024-10-10", "Salão", 50.0)
        self.controller.adicionar_evento(evento)
        usuario = self.controller.usuarios[0]
        feedback = usuario.avaliar_evento(evento, 5, "Ótimo evento!")
        self.assertEqual(feedback.nota, 5)
        self.assertEqual(feedback.comentario, "Ótimo evento!")

if __name__ == "__main__":
    unittest.main()