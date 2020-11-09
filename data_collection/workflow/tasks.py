from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable

from data_collection.database.models import (
    shelf_items_table,
    shelves_table,
    stores_table,
)
from data_collection.scraping.spiders.instacart.spider import InstacartSpider


async def instacart_collect():
    spider = InstacartSpider()
    return await spider.crawl()


async def db_create_tables(dsn):
    async with create_engine(dsn) as engine:
        async with engine.acquire() as conn:
            await conn.execute(
                "DROP TABLE IF EXISTS stores, shelves, shelf_items CASCADE"
            )
            await conn.execute(CreateTable(stores_table))
            await conn.execute(CreateTable(shelves_table))
            await conn.execute(CreateTable(shelf_items_table))


async def db_load(dsn, store_data):
    async with create_engine(dsn) as engine:
        async with engine.acquire() as conn:
            shelves = store_data.pop("shelves")

            store_insert = stores_table.insert().values(**store_data)
            store_id = await conn.scalar(store_insert)

            for entry in shelves:
                items = entry.pop("shelf_items")

                entry["store_id"] = store_id
                shelf_insert = shelves_table.insert().values(**entry)
                shelf_id = await conn.scalar(shelf_insert)

                shelf_items = [
                    {"item_name": name, "shelf_id": shelf_id} for name in items
                ]
                for item in shelf_items:
                    shelf_item_insert = shelf_items_table.insert().values(**item)
                    await conn.execute(shelf_item_insert)
