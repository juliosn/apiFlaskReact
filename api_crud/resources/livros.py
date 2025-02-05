from flask_restful import Resource, reqparse
from models.livros import LivroModel

class Livro(Resource):
    def get(self, id=None):
        if id:
            livro = LivroModel.query.get(id)
            if livro:
                return livro.json()
            return {'message': 'Livro nao encontrado'}, 404
        else:
            livros = LivroModel.query.all()
            return [livro.json() for livro in livros], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', required=True, help="Nome nao pode ser vazio")
        parser.add_argument('autor', required=True, help="Autor nao pode ser vazio")
        parser.add_argument('ano', type=int, required=True, help="O ano nao pode ser vazio")
        parser.add_argument('preco', type=float, required=True, help="O preco nao pode ser vazio")
        
        dados = parser.parse_args()

        if not dados['nome'] or dados['nome'] is None:
            return {'message': 'Nome nao pode ser vazio'}, 400
        if not dados['autor'] or dados['autor'] is None:
            return {'message': 'Autor nao pode ser vazio'}, 400
        if dados['ano'] is None:
            return {'message': 'Ano nao pode ser vazio'}, 400
        if dados['preco'] is None:
            return {'message': 'Preço nao pode ser vazio'}, 400

        cliente = LivroModel(**dados)
        cliente.save_to_db()

        return cliente.json(), 201

    def put(self, id):
        livro = LivroModel.query.get(id)
        if not livro:
            return {'message': 'Livro nao encontrado'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('nome', required=True, help="Nome nao pode ser vazio")
        parser.add_argument('autor', required=True, help="Autor nao pode ser vazio")
        parser.add_argument('ano', type=int, required=True, help="O ano nao pode ser vazio")
        parser.add_argument('preco', type=float, required=True, help="O preco nao pode ser vazio")
        
        dados = parser.parse_args()

        if not dados['nome'] or dados['nome'] is None:
            return {'message': 'Nome nao pode ser vazio'}, 400
        if not dados['autor'] or dados['autor'] is None:
            return {'message': 'Autor nao pode ser vazio'}, 400
        if dados['ano'] is None:
            return {'message': 'Ano nao pode ser vazio'}, 400
        if dados['preco'] is None:
            return {'message': 'Preço nao pode ser vazio'}, 400

        livro.nome = dados['nome']
        livro.autor = dados['autor']
        livro.ano = dados['ano']
        livro.preco = dados['preco']
        livro.save_to_db()

        return livro.json(), 200

    def delete(self, id):
        livro = LivroModel.query.get(id)
        if not livro:
            return {'message': 'Livro nao encontrado'}, 404

        livro.delete_from_db()
        return {'message': 'Livro excluido'}, 200
