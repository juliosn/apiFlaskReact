import unittest
import sys
import os
from flask import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from sql_alchemy import banco
from models.livros import LivroModel

class TestLivroAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.testing = True
        
        banco.init_app(app)
        cls.app = app.test_client()

        with app.app_context():
            banco.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            banco.session.remove()
            banco.drop_all()

    def tearDown(self):
        with app.app_context():
            banco.session.rollback()
            for table in reversed(banco.metadata.sorted_tables):
                banco.session.execute(table.delete())
            banco.session.commit()

    def test_get_all_livros(self):
        response = self.app.get('/api/v1/livros')
        self.assertEqual(response.status_code, 200)

    def test_create_livro(self):
        data = {
            'nome': 'Novo Livro',
            'autor': 'Novo Autor',
            'ano': 2008,
            'preco': 200.0
        }
        response = self.app.post('/api/v1/livros', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Novo Livro', response.data.decode())

    def test_delete_livro(self):
        with app.app_context():
            livro = LivroModel(nome='Livro Deletado', autor='Autor Deletado', ano=2000, preco=50.0)
            banco.session.add(livro)
            banco.session.commit()
            banco.session.refresh(livro)

        response = self.app.delete(f'/api/v1/livros/{livro.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Livro excluido', response.data.decode())

    def test_get_livro(self):
        with app.app_context():
            livro = LivroModel(nome='Teste Livro', autor='Autor Teste', ano=2022, preco=99.99)
            banco.session.add(livro)
            banco.session.commit()
            banco.session.refresh(livro)

        response = self.app.get(f'/api/v1/livros/{livro.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Teste Livro', response.data.decode())

    def test_update_livro(self):
        with app.app_context():
            livro = LivroModel(nome='Livro Antigo', autor='Autor Antigo', ano=1999, preco=80.0)
            banco.session.add(livro)
            banco.session.commit()
            banco.session.refresh(livro)

        data = {
            'nome': 'Livro Atualizado',
            'autor': 'Autor Atualizado',
            'ano': 2021,
            'preco': 150.0
        }

        response = self.app.put(f'/api/v1/livros/{livro.id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Livro Atualizado', response.data.decode())

    def test_create_livro_invalid_data(self):
        data = {
            'nome': '',
            'autor': 'Autor Incompleto',
            'ano': 2020,
            'preco': 50.0
        }
        response = self.app.post('/api/v1/livros', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Nome nao pode ser vazio', response.data.decode())

    def test_get_non_existent_livro(self):
        response = self.app.get('/api/v1/livros/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Livro nao encontrado", response.data.decode())

    def test_delete_non_existent_livro(self):
        response = self.app.delete('/api/v1/livros/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Livro nao encontrado', response.data.decode())

    def test_update_non_existent_livro(self):
        response = self.app.put('/api/v1/livros/999', json={'nome': 'Livro Falso', 'autor': 'Fake', 'ano': 2020, 'preco': 99.99})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Livro nao encontrado', response.data.decode())

    def test_create_livro_missing_required_field(self):
        data = {
            'autor': 'Autor Sem Nome',
            'ano': 2020,
            'preco': 200.0
        }
        response = self.app.post('/api/v1/livros', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Nome nao pode ser vazio', response.data.decode())

if __name__ == '__main__':
    unittest.main()
