# ModelConnect

ModelConnect is a library that enables users to connect their dataclass models with other libraries
without writing additional boilerplate code.

ModelConnect goals and how it achieves them:

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
        ...
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

Let's start with the following project architecture that uses FastAPI and psycopg2 to create a CRUD API:

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
from model_connect import connect


@dataclass
class User:
    name: str
    age: int


connect(User)
```

Let's also configure the `db.py` module. This exposes a function that returns a new database connection.

```python
# db.py

from psycopg2 import connect


def open_db_connection():
    return connect('...')  # pass in custom DB details
```

Now, with our models setup,
we can use these throughout our application and start replacing the boilerplate.

Normally, most CRUD apps that follow N-tier architecture will have the following modules:

- `controller.py` - used for API endpoint routing
- `service.py` - used for business logic and validation
- `repository.py` - used for abstracting database CRUD operations

From a minimal setup perspective, everything we need is in our model.
Therefore, we can remove the `service.py` and `repository.py` modules and just use the `controller.py`.

NOTE: This is not to say that the `service.py` and `repository.py` modules are not useful.
In fact, most complex applications will use these modules to handle unique business logic.
But what this is demonstrating is that for a simple setup (where most of the code in these layers are boilerplate),
you can remove these modules and just use the model as the scaffolding.

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

Done!

And just like that, you've created CRUD API that exposes several endpoints for your `User` resource.
Normally, writing the DTOs, and the duplicate models (Pydantic, ORMs, etc.) would have taken hundreds of lines of code.
But with ModelConnect, you're given functions that auto generate this functionality for you.

NOTE: Notice how ModelConnect does not assume the database or the API framework you are using.
This is done purposely to allow you to swap out the database or API framework at any time.
In the case you wanted to remove the boilerplate code even further,
you can create your own functions that wraps a series of ModelConnect functions for you.

# Library Support

API Frameworks:

- FastAPI
- Flask *(Coming Soon)*
- Django *(Coming Soon)*

Database Libraries:

- Psycopg2
- SQLAlchemy *(Coming Soon)*
- PyMongo *(Coming Soon)*
- PyMySQL *(Coming Soon)*

Validation Libraries:

- Pydantic *(Coming Soon)*
- Marshmallow *(Coming Soon)*

Serialization

- JSON *(Coming Soon)*
- YAML *(Coming Soon)*

# Build Your Own Integrations

## Understanding the Options Chain

When a model is connected, it goes through a series of resolutions.
These resolutions are referred to as the Options Chain.
Their purpose is to propagate the default behaviour down the options tree
where deeper nodes define more specific behaviour.
The order is as follows:

```
# called once per project (not yet implemented)
connect_globals
|-- GlobalOptions
    |-- Model
    |   |-- Integrations
    |       |-- Integration
    |-- ModelFields
        |-- ModelField
            |-- Dtos
                |-- Dto
            |-- Validator
            |-- Integrations
                |-- Intgration

...

# called on each model
connect
|-- ConnectOptions
    |-- Model
    |   |-- Integrations
    |       |-- Integration
    |-- ModelFields
        |-- ModelField
            |-- Dtos
                |-- Dto
            |-- Validator
            |-- Integrations
                |-- Intgration
```

When `connect(...)` is called, a few things happen:

1. ConnectOptions is created (if not already)
2. `ConnectOptions.resolve()` is called

When `ConnectOptions.resolve` is called, a few (more) things happen:

1. Model is created (if not already)
2. ModelFields is created (if not already)
3. `Model.resolve()` is called
4. `ModelFields.resolve()` is called

This continues down the tree until all nodes are resolved.

If you are familiar with pre-order DFS traversal, this is essentially what is happening.
The "pre-order" functionality is the `resolve()` method.
By resolving the nodes in this way, downstream nodes have access to the default behaviour of upstream nodes
and can override them if necessary.

## Examples

You can see this model chain concept in action when you connect a model:

```python
from dataclasses import dataclass
from model_connect import connect
from model_connect.options import ConnectOptions, Model, ModelFields, ModelField
from model_connect.integrations.psycopg2 import Psycopg2Model


@dataclass
class User:
    name: str
    age: int


connect(
    User,
    ConnectOptions(
        model=Model(
            override_integrations=(
                Psycopg2Model(
                    tablename='users'
                    # <- overrides the default behaviour which is snake_case from dataclass name ('user')
                ),
            )
        ),
        fields=ModelFields(
            id=ModelField(
                is_identifier=True,
                # <- metadata. downstream nodes (i.e. psycopg2) use this value to determine behaviour
                validators=(),  # <- validators
                dtos=(),  # <- dtos
                # integrations=(...),  # <- no overrides so integrations will attempt to infer attributes from previous options
            ),
            name=ModelField(),
            # age=ModelField(), # <- not specified so ModelFields will attempt to infer attributes from dataclass
        )
    )
)
```

In another case,
you may not need to override the inferred behaviour from the dataclass.
Then, you just connect the model without any options
and the same option chain will handle constructing the options with the defaults:

```python
from dataclasses import dataclass
from model_connect import connect


@dataclass
class User:
    name: str
    age: int


connect(User)  # <- The options (ConnectOptions, Mode, etc.) are inferred from the dataclass
```

# Developer Guide

To rebuild distribution:

```bash
python setup.py sdist
```

To upload to PyPi:

```bash
twine upload dist/*
```

To do both:
    
```bash
python setup.py sdist
twine upload dist/*
```

## Contributing

TBD

# Q&A

## Library or a framework?

The goal was not to create another framework.

Instead, the goal is to create a library that handles the integration of multiple frameworks / libraries.

## Why dataclasses?

It's part of the Python standard library.
Other model libraries may be supported in the future later.
