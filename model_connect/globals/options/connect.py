from dataclasses import dataclass
from typing import Optional

from model_connect.constants import UNDEFINED, coalesce
from model_connect.globals.options.fastapi import FastAPIGlobalOptions
from model_connect.globals.options.psycopg2 import Psycopg2GlobalOptions


@dataclass
class GlobalConnectOptions:
    psycopg2: Optional[Psycopg2GlobalOptions] = UNDEFINED
    fastapi: Optional[FastAPIGlobalOptions] = UNDEFINED

    @property
    def integrations(self):
        return {
            'psycopg2': self.psycopg2,
            'fastapi': self.fastapi
        }

    def resolve(self):
        self.psycopg2 = coalesce(
            self.psycopg2,
            Psycopg2GlobalOptions()
        )

        self.fastapi = coalesce(
            self.fastapi,
            FastAPIGlobalOptions()
        )

        self.psycopg2.resolve()
        self.fastapi.resolve()
