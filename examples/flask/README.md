# Flask

Flask is a lightweight WSGI web application framework, and it's also a good option
for writing RESTful APIs.


## Installation

```
$ pip install -r requirements.txt
$ flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

See the [top level README](https://github.com/pallets-eco/flask-api-examples#readme)
for the environment setup and how to play with the API.


## Introduction

Flask provides some route shortcuts for web APIs:

- `app.get()`
- `app.post()`
- `app.put()`
- `app.patch()`
- `app.delete()`

So the following usage:

```python
@app.route('/pets', methods=['POST'])
def create_pet():
    pass
```

Can be simplified to:

```python
@app.post('/pets')
def create_pet():
    pass
```

With `flask.views.MethodView`, you can also organize the APIs with class. Each
method of the class maps to the corresponding HTTP method when dispatching
the request to this class:

```python
from flask.views import MethodView


class PetResource(MethodView):

    def get(self):
        pass

    def patch(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


app.add_url_rule('/pets/<int:pet_id>', view_func=PetResource.as_view('pet'))
```

See more details in [Method Based Dispatching](https://flask.palletsprojects.com/views/#method-based-dispatching).


## Resources

- Documentation: https://flask.palletsprojects.com/
- Source code: https://github.com/pallets/flask/
- Chat: https://discord.gg/pallets
