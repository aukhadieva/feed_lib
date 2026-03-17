from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

BaseDBModel = declarative_base()

class TestModelDB(BaseDBModel):
    """Test database model."""
    __tablename__ = 'test_model'
    __table_args__ = {'schema': 'lib'}

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

class Test2ModelDB(BaseDBModel):
    """Test database model."""
    __tablename__ = 'test2_model'
    __table_args__ = {'schema': 'lib'}

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
