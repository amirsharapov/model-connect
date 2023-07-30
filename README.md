# ModelConnect

ModelConnect is a library that enables users to connect their dataclass models with other libraries 
without writing additional boilerplate code.

Our goals and how we plan to achieve them:

- Simplicity
  - Fluent API
  - Minimal Setup to Start


- Reliability
  - Tested & Testable
  - Type Annotated


- Extensible
  - Custom Library Adapters & Functions Builder
    - Includes testing utilities
  - Override all behaviours

## Before ModelConnect

```
- src/
  - ...
  - features/
    - user/
      - routes.py         # API routing
      - service.py        # business logic
      - models/
        - orm.py          # i.e. sqlalchemy (only required if using ORM libraries)
        - dtos.py         # i.e. pydantic, marshmallow (almost always required)
        - bl.py           # i.e. pydantic, dataclasses (can replace with other models, but recommended)
        - ui.py           # i.e. flask app builder (only required if using UI libraries)
```

## After ModelConnect

```
- src/
  - ...
  - features/
    - user/
      - routes.py         # API routing
      - service.py        # business logic
      - model.py          # Plain old dataclass objects
```

# Quick Start

For example purposes, let's start with the following repository architecture:

```
- src/
    - db.py
    - models.py
    - routes.py
- main.py
```

Inside the `models.py` module, we define our models using dataclasses

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str


@dataclass
class UserAddress:
    user: User
    address: Address
```

Now, with our models setup,
we can use these throughout our application and start replacing the boilerplate.

Let's also configure the `db.py` module:

```python
# db.py

from psycopg2 import connect

def open_db_connection():
    return connect('...') # pass in custom DB details
```

Now let's get to the boilerplate code.
Normally, most CRUD apps that follow N-tier architecture will have the following modules:

- controller.py  # used for API endpoint routing
- service.py  # used for business logic and validation
- repository.py  # used for abstracting database CRUD operations

In our case, because we've defined everything we technically need in our model,
we can replace all of these modules with a single `routes.py` module.

```python
from fastapi import Depends
from model_connect.integrations.fastapi import (
    create_router,
    create_response_dtos,
    create_response_dto,
    get_from_post_request_dto,
    get_from_post_request_dtos,
    get_from_put_request_dto,
    get_from_patch_request_dto,
    get_filter_options,
    get_pagination_options,
    get_sort_options
)
from model_connect.integrations.psycopg2 import (
    stream_select,
    stream_insert,
    stream_update,
    stream_partial_update,
    stream_delete,
)

from src.models import User
from src.db import open_db_connection

router = create_router(User)

@router.get('')
def get_users(
        filter_options: dict = Depends(get_filter_options(User)),
        pagination_options: dict = Depends(get_pagination_options(User)),
        sort_options: dict = Depends(get_sort_options(User))
):
    connection = open_db_connection()
    with connection.cursor() as cursor:
          return create_response_dtos(
                stream_select(
                    User,
                    cursor,
                    filter_options=filter_options,
                    pagination_options=pagination_options,
                    sort_options=sort_options
                )
          )


@router.get('/{resource_id}')
def get_user(resource_id: int):
    connection = open_db_connection()
    with connection.cursor() as cursor:
          return create_response_dto(
                stream_select(
                    User,
                    cursor,
                    filter_options={'id': resource_id}
                )
          )


@router.post('')
def post_user(user: Depends(get_from_post_request_dto(User))):
    connection = open_db_connection()
    with connection.cursor() as cursor:
        return create_response_dto(
            stream_insert(
                cursor,
                user
            )
        )


@router.post('/bulk')
def post_users(users: Depends(get_from_post_request_dto(User))):
    connection = open_db_connection()
    with connection.cursor() as cursor:
        return create_response_dtos(
            stream_insert(
                cursor, 
                users,
            )
        )


@router.put('/{resource_id}')
def put_user(user: Depends(get_from_put_request_dto(User))):
    connection = open_db_connection()
    with connection.cursor() as cursor:
        return create_response_dto(
            stream_update(
                cursor,
                user
            )
        )


@router.patch('/{resource_id}')
def patch_user(user: Depends(get_from_patch_request_dto(User))):
    connection = open_db_connection()
    with connection.cursor() as cursor:
        return create_response_dto(
            stream_partial_update(
                cursor,
                user
            )
        )


@router.delete('/{resource_id}')
def delete_user(resource_id: int):
    connection = open_db_connection()
    with connection.cursor() as cursor:
        return create_response_dto(
            stream_delete(
                cursor,
                User,
                filter_options={
                    'id': resource_id
                }
            )
        )
```

That's it! Now let's go over what each section of the code does.

# Custom Configurations

Now you may ask,
how do I actually integrate this with all the other libraries I'm using?

# Build Your Own

When a model is connected, it goes through a series of resolutions.
These resolutions propagate the default behaviour down the chain of specificities.
The order is as follows:

1. Connect Options `resolve(model_class)`
2. Model | ModelField Options `resolve(model_class, connect_options)`
3. Library Options `resolve(model_class, connect_options, model_options)`

The ConnectOptions contains metadata used by the model-connect library not specific to the model.
Next, the Model and Field options are specific to the model and fields and apply to all integrations.
Finally, there are library-specific options that are specific to the library integration and
provide the user full control on how the model behaviour with the library.

Consider this a pre-order DFS traversal of the model tree.

## Model

This is the dataclass that you define. It contains the fields that are to be used.

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
```

In the example above, the user is the model.

## ModelConnect Options

These are the options that you can pass into the `connect` function.

```python
from dataclasses import dataclass
from model_connect import connect
from model_connect.options import ConnectOptions, Model, ModelFields, ModelField


@dataclass
class User:
  id: int
  name: str
  age: int


connect(
  User,
  ConnectOptions(
    model=Model(
      overrides=(
        Pscyopg2Integration(
          tablename='users'
        ),
      )
    ),
    fields=ModelFields(
      id=ModelField(
        is_identifier=True,
        is_required=True,
        overrides=(
          Pscyopg2Integration(
            columnname='id'
          ),
        ),
      ),
      name=ModelField(
        is_required=True
      ),
      age=ModelField(
        is_required=True
      )
    )
  )
)
```

## Supported Libraries

API Frameworks:
- FastAPI
- Flask
- Django *(TBD)*

Database Libraries:
- SQLAlchemy
- Psycopg2
- PyMongo *(TBD)*
- PyMySQL *(TBD)*

Validation Libraries:
- Pydantic
- Marshmallow

Serialization
- JSON
- YAML

# Contributing

TBD

# Q&A

## Library or a framework?

With the exception of setting up the initial dataclass models,
ModelConnect does not force you to write your code a specific way.

Once you've connected the model, you can use it like a normal dataclass.

The exception here is, if a framework requires additional functionality
or you wish to provide extra specification, you can do so.

## Why dataclasses?

It's part of the Python standard library.
