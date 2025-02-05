from sql_alchemy import banco

class LivroModel(banco.Model):
    __tablename__ = 'livros'

    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100))
    autor = banco.Column(banco.String(100))
    ano = banco.Column(banco.Integer)
    preco = banco.Column(banco.Float)

    def __init__(self, nome, autor, ano, preco):
        self.nome = nome
        self.autor = autor
        self.ano = ano
        self.preco = preco

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'autor': self.autor,
            'ano': self.ano,
            'preco': self.preco
        }

    def save_to_db(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_from_db(self):
        banco.session.delete(self)
        banco.session.commit()
