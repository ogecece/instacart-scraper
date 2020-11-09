from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)

metadata = MetaData()

stores_table = Table(
    "stores",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("store_name", String, unique=True, nullable=False),
    Column("store_logo_url", String),
)

shelves_table = Table(
    "shelves",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("shelf_name", String, nullable=False),
    Column("store_id", Integer, ForeignKey("stores.id")),
    UniqueConstraint("shelf_name", "store_id"),
)


shelf_items_table = Table(
    "shelf_items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("item_name", String, nullable=False),
    Column("shelf_id", Integer, ForeignKey("shelves.id")),
    UniqueConstraint("item_name", "shelf_id"),
)
