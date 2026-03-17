from sqlalchemy.orm import Mapped, mapped_column

from feed_lib.base.models import BaseDBModel


class TestModelDB(BaseDBModel):
    """Test database model."""
    __tablename__ = 'test_model'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class Test2ModelDB(BaseDBModel):
    """Test database model."""
    __tablename__ = 'test2_model'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
