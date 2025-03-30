import factory
from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory as PModelFactory
from polyfactory.factories.pydantic_factory import T

from tests import TestingSessionLocal


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        # https://factoryboy.readthedocs.io/en/stable/orms.html#managing-sessions
        sqlalchemy_session = TestingSessionLocal
        sqlalchemy_session_persistence = "flush"


class ModelFactory(PModelFactory[T]):
    __is_base_factory__ = True

    @classmethod
    def build_invalid_data(cls) -> dict:
        fake_value = Faker().pydict(nb_elements=2)
        return {field: fake_value for field in cls.__model__.__fields__.keys()}

    @classmethod
    def build_invalid_fields(cls) -> dict:
        return {
            f"{key}_{Faker().pyint()}": value
            for key, value in cls.build().dict().items()
        }
