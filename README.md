# ModelConnect

ModelConnect is a library that enables users to connect their dataclass models with other libraries 
without writing additional boilerplate code.

Our goals and how we plan to achieve them:

- Simplicity
  - Fluent API
  - Minimal Boilerplate to start


- Reliability
  - Test module to test model configurations
  - Explicit parameters
  - Consistent error messages & return types


- Extensible
  - Custom Library Adapters Builder
  - Custom Library Functions Builder
  - Override most config behaviours

## Before ModelConnect

```
- src/
  - ...
  - features/
    - user/
      - routes.py         # API routing
      - service.py        # business logic
      - models/
        - orm.py          # sqlalchemy, etc.
        - dtos.py         # pydantic, etc.
        - bl.py           # pydantic, etc.
        - ui.py           # flask app builder, etc.
```

## After ModelConnect

```
- src/
  - ...
  - features/
    - user/
      - routes.py         # API routing
      - service.py        # business logic
      - model.py          # One (dataclass) model to rule them all
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
        filter_options: dict = Depends(get_filter_options()),
        pagination_options: dict = Depends(get_pagination_options()),
        sort_options: dict = Depends(get_sort_options())
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

# Build Your Own Library Integrations

TBD

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
