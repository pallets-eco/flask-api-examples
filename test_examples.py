from importlib import reload
import sys

import pytest

examples = [
    'flask',
]


@pytest.fixture
def client(request):
    app_path = f'examples/{request.param}'
    sys.path.insert(0, app_path)
    import app
    app = reload(app)
    _app = app.app
    _app.testing = True
    sys.path.remove(app_path)
    return _app.test_client()


@pytest.mark.parametrize('client', examples, indirect=True)
def test_say_hello(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.json
    assert rv.json['message'] == 'Hello!'


@pytest.mark.parametrize('client', examples, indirect=True)
def test_get_pet(client):
    rv = client.get('/pets/1')
    assert rv.status_code == 200
    assert rv.json
    assert rv.json['name'] == 'Kitty'
    assert rv.json['category'] == 'cat'

    rv = client.get('/pets/13')
    assert rv.status_code == 404
    assert rv.json


@pytest.mark.parametrize('client', examples, indirect=True)
def test_get_pets(client):
    rv = client.get('/pets')
    assert rv.status_code == 200
    assert rv.json
    assert len(rv.json['pets']) == 3
    assert rv.json['pets'][0]['name'] == 'Kitty'
    assert rv.json['pets'][0]['category'] == 'cat'


@pytest.mark.parametrize('client', examples, indirect=True)
def test_create_pet(client):
    rv = client.post('/pets', json={
        'name': 'Grey',
        'category': 'cat'
    })
    assert rv.status_code == 201
    assert rv.json
    assert rv.json['name'] == 'Grey'
    assert rv.json['category'] == 'cat'


@pytest.mark.parametrize('client', examples, indirect=True)
@pytest.mark.parametrize('data', [
    {'name': 'Grey', 'category': 'human'},
    {'name': 'Fyodor Mikhailovich Dostoevsky', 'category': 'cat'},
    {'category': 'cat'},
    {'name': 'Grey'}
])
def test_create_pet_with_bad_data(client, data):
    rv = client.post('/pets', json=data)
    assert rv.status_code == 400
    assert rv.json


@pytest.mark.parametrize('client', examples, indirect=True)
def test_update_pet(client):
    new_data = {
        'name': 'Ghost',
        'category': 'dog'
    }

    rv = client.patch('/pets/1', json=new_data)
    assert rv.status_code == 200
    assert rv.json

    rv = client.get('/pets/1')
    assert rv.status_code == 200
    assert rv.json['name'] == new_data['name']
    assert rv.json['category'] == new_data['category']

    rv = client.patch('/pets/13', json=new_data)
    assert rv.status_code == 404
    assert rv.json


@pytest.mark.parametrize('client', examples, indirect=True)
@pytest.mark.parametrize('data', [
    {'name': 'Fyodor Mikhailovich Dostoevsky'},
    {'category': 'human'}
])
def test_update_pet_with_bad_data(client, data):
    rv = client.patch('/pets/1', json=data)
    assert rv.status_code == 400
    assert rv.json


@pytest.mark.parametrize('client', examples, indirect=True)
def test_delete_pet(client):
    rv = client.delete('/pets/1')
    assert rv.status_code == 204

    rv = client.get('/pets/1')
    assert rv.status_code == 404
    assert rv.json

    rv = client.delete('/pets/13')
    assert rv.status_code == 404
    assert rv.json
