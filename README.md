# About

ModelConnect is a library that enables users to connect their dataclass models with other libraries 
without writing additional boilerplate code.

Our focus here is on simplicity, IOC, and developer experience.

From a business perspective, our goal is to
enable developers to focus on the business logic of their application
and spend less time writing code.

From a developer experience perspective, our goal is to
write an easy-to-use, easy-to-follow, and-easy-to-extend library


# Get Started

Inside the `models.py` module, we define our models and connect them with ModelConnect.
```python
from dataclasses import dataclass
from model_connect import connect

@dataclass
class User:
    name: str
    age: int


# We call a function to connect our model with the registry
connect(User)
```

Now, with our model setup, we can use them in our application as we normally would.
In our case, let's setup a REST API with the following directory structure:

```
- src/
    - db.py
    - dao.py
    - models.py
    - routes.py
- main.py
```

and start replacing the boilerplate.

Note: We are purposely skipping the service layer as we want to focus on layers where
boilerplate is prominent. The service layer ideally contains business logic and therefore,
should not have much boilerplate as other areas.

Let's start with where every request in our app begins:

```python
from fastapi import FastAPI
from model_connect.adapters.fastapi import create_router
from model_connect.adapters.fastapi.dependencies import (
    get_response_dtos,
    get_filter_options,
    get_pagination_options,
    get_sort_options
)

```

```python
from model_connect.adapters.psycopg2 import (
    stream_select,
    stream_insert,
    stream_update,
    stream_delete,
)

from src.models import User
from src.db import get_connection


def get():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            return stream_select(
                cursor,
                User
            )


def get_by_id():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            return next(stream_select(cursor, User), None)
```

Our routes.py

```python
from model_connect.adapters.fastapi import create_router
from model_connect_custom__library_name__adapters import (
    MyCustomAdapter,
    adapter_function_1,
    adapter_function_2,
    adapter_function_3
)

from src.models import User
from src.services import user as service

router = create_router(User)


@router.get()
def get_users():
    return get_response_dtos(service.get())


@router.delete()
def delete_user():
    user = service.delete()

    return {
        'id': user.id
    }
```

# Anticipated Questions

## Library or a framework?

With the exception of setting up the initial dataclass models,
ModelConnect does not force you to write your code a specific way.

Once you've connected the model, you can use it like a normal dataclass.

The exception here is, if a framework requires additional functionality
or you wish to provide extra specification, you can do so.

## Why dataclasses?

It's part of the Python standard library.
