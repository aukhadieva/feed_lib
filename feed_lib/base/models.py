import uuid
import warnings
from datetime import datetime
from typing import Any

from sqlalchemy import BIGINT, TIMESTAMP, String, func, ForeignKey, JSON, ARRAY, Column, UUID, exc, event, Table, DDL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TypeDecorator, CHAR

warnings.filterwarnings('ignore',
                        category=exc.SAWarning,
                        message='.*Class Select will not make use of SQL compilation caching.*'
                        )

FK = ForeignKey
mc = mapped_column
c = Column


class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        """Load dialect."""
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(CHAR(32))
        return dialect.type_descriptor(UUID())

    def process_bind_param(self, value, dialect):
        """Process bind param."""
        if value is not None:
            if dialect.name == 'sqlite':
                if not isinstance(value, uuid.UUID):
                    return "%.32x" % uuid.UUID(value).int
                return "%.32x" % value.int
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        """Process result value."""
        if value is not None and not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value


class BaseDBModel(DeclarativeBase):
    """Base PostgresQL database model."""
    __abstract__ = True
    __allow_unmapped__ = True
    __table_args__ = {'schema': 'lib'}

    type_annotation_map = {
        UUID: GUID(),
        int: BIGINT,
        datetime: TIMESTAMP(timezone=True),
        str: String(),
        dict[str, Any]: JSON,
        list[UUID]: ARRAY(UUID()),
        list[str]: ARRAY(String()),
    }

    uuid: Mapped[GUID | UUID] = mc(GUID(), primary_key=True, default=uuid.uuid4)
    create_date: Mapped[datetime] = mc(server_default=func.now())
    update_date: Mapped[datetime] = mc(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        repr_text = super().__repr__()
        return f'{repr_text[:-1]}, {self.uuid}>'


@event.listens_for(Table, 'after_parent_attach')
def create_schema(table: Table, _):
    """Create schema."""
    schema = table.schema
    if schema:
        event.listen(table, 'before_create', DDL(f'CREATE SCHEMA IF NOT EXISTS {schema}'))
