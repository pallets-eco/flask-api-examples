from flask import Flask, request
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy

PET_CATEGORIES = ['cat', 'dog']
PET_REQUIRED_FIELD_ERROR = 'The name and category field is required.'
PET_NAME_LENGTH_ERROR = 'The length of the name must be between 0 and 10.'
PET_CATEGORY_ERROR = 'The category must be one of: dog, cat.'
PET_ID_ERROR = 'Pet not found.'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class PetModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    category = db.Column(db.String(10))


@app.before_first_request
def init_database():
    """Create the table and add some fake data."""
    pets = [
        {'name': 'Kitty', 'category': 'cat'},
        {'name': 'Coco', 'category': 'dog'},
        {'name': 'Flash', 'category': 'cat'}
    ]
    db.create_all()
    for pet_data in pets:
        pet = PetModel(**pet_data)
        db.session.add(pet)
    db.session.commit()


@app.errorhandler(HTTPException)
def handle_http_errors(error):
    return {'message': error.name}, error.code


def pet_schema(pet):
    return {
        'id': pet.id,
        'name': pet.name,
        'category': pet.category
    }


@app.get('/')
def say_hello():
    return {'message': 'Hello!'}


@app.get('/pets/<int:pet_id>')
def get_pet(pet_id):
    pet = PetModel.query.get(pet_id)
    if pet is None:
        return {'message': PET_ID_ERROR}, 404
    return pet_schema(pet)


@app.get('/pets')
def get_pets():
    pets = PetModel.query.all()
    return {'pets': [pet_schema(pet) for pet in pets]}


@app.post('/pets')
def create_pet():
    data = request.json
    if 'name' not in data or 'category' not in data:
        return {'message': PET_REQUIRED_FIELD_ERROR}, 400
    if len(data['name']) > 10:
        return {'message': PET_NAME_LENGTH_ERROR}, 400
    if data['category'] not in PET_CATEGORIES:
        return {'message': PET_CATEGORY_ERROR}, 400

    pet = PetModel(name=data['name'], category=data['category'])
    db.session.add(pet)
    db.session.commit()
    return pet_schema(pet), 201


@app.patch('/pets/<int:pet_id>')
def update_pet(pet_id):
    pet = PetModel.query.get(pet_id)
    if pet is None:
        return {'message': PET_ID_ERROR}, 404

    data = request.json
    if 'name' in data:
        if len(data['name']) > 10:
            return {'message': PET_NAME_LENGTH_ERROR}, 400
        else:
            pet.name = data['name']
    if 'category' in data:
        if data['category'] not in PET_CATEGORIES:
            return {'message': PET_CATEGORY_ERROR}, 400
        else:
            pet.category = data['category']
    db.session.commit()
    return pet_schema(pet)


@app.delete('/pets/<int:pet_id>')
def delete_pet(pet_id):
    pet = PetModel.query.get(pet_id)
    if pet is None:
        return {'message': PET_ID_ERROR}, 404
    db.session.delete(pet)
    db.session.commit()
    return '', 204
