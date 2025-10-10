class Feedback:
    def __init__(self, usuario, evento, nota: int, comentario: str, data):
        self.usuario = usuario 
        self.evento = evento    
        self.nota = nota        
        self.comentario = comentario  
        self.data = data     

    def __repr__(self):
        return f"Feedback(usuario={self.usuario.nome}, evento={self.evento.nome}, nota={self.nota}, comentario={self.comentario}, data={self.data})"