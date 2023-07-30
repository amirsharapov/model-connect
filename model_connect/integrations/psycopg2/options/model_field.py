from model_connect.integrations.base import BaseIntegrationModelField


class Psycopg2ModelField(BaseIntegrationModelField):
    def __init__(
            self,
            *args,
            can_filter: bool = True,
            can_sort: bool = True,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.can_filter = can_filter
        self.can_sort = can_sort
