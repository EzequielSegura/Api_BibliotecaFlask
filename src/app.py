from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config

def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    return app
enviroment = config['development']
app = create_app(enviroment)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Libros(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), unique=True)
    autor = db.Column(db.String(100))

    def __init__(self, isbn, titulo, autor):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
db.create_all()

class LibroSchema(ma.Schema):
    class Meta:
        fields = ('isbn', 'titulo', 'autor')
libro_schema = LibroSchema()
libros_schema = LibroSchema(many=True)

@app.route('/libros', methods=['Post'])
def create_libro():
    isbn = request.json['isbn']
    titulo = request.json['titulo']
    autor = request.json['autor']
    new_libro = Libros(isbn, titulo, autor)
    db.session.add(new_libro)
    db.session.commit()
    return libro_schema.jsonify(new_libro)

@app.route('/libros/', methods=['GET'])
def get_libros():
    todos_libros = Libros.query.all()
    result = libros_schema.dump(todos_libros)
    return jsonify(result)

@app.route('/libros/<isbn>', methods=['GET'])
def get_libro(isbn):
    libro = Libros.query.get(isbn)
    return libro_schema.jsonify(libro)

@app.route('/libros/<isbn>', methods=['PUT'])
def update_libro(isbn):
    libro = Libros.query.get(isbn)
    isbn = request.json['isbn']
    titulo = request.json['titulo']
    autor = request.json['autor']
    libro.isbn = isbn
    libro.titulo = titulo
    libro.autor = autor
    db.session.commit()
    return libro_schema.jsonify(libro)

@app.route('/libros/<isbn>', methods=['DELETE'])
def delete_libro(isbn):
    libro = Libros.query.get(isbn)
    db.session.delete(libro)
    db.session.commit()
    return libro_schema.jsonify(libro)


@app.route('/', methods=['GET'])
def index():
    doc = jsonify({'message': 'Welcome to my API'}, {'/libros': 'Ver todos los libros'}, {'/libros/(ISBN)': 'Buscar libro por ISBN'})
    
    return doc

if __name__ == "__main__":
    app.run(debug=True)