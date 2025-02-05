from flask import Flask
from flask_restful import Api
from flask_cors import CORS  # Importa o Flask-CORS
from resources.livros import Livro
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.before_request
def cria_banco():
    banco.create_all()

api.add_resource(Livro, '/api/v1/livros', '/api/v1/livros/<int:id>')

if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True, port=5001)
