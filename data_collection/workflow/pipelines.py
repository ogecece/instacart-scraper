import logging
import traceback

from data_collection.exceptions import ExecutionFailedException
from data_collection.settings import DB_DSN

from .tasks import db_create_tables, db_load, instacart_collect

logger = logging.getLogger(__name__)


async def instacart_shelves():
    db_dsn = DB_DSN
    await db_create_tables(db_dsn)
    logger.info("Tables created.")

    for retry_attempt in range(5):
        logger.info(f"Running Instacart spider. Attempt #{retry_attempt+1}")
        try:
            entries = await instacart_collect()
        except:
            traceback.print_exc()
        else:
            break
    else:
        raise ExecutionFailedException(
            "Couldn't collect Instacart's info right now. Try again later."
        )

    logger.info(f"Spider run successfully!")
    logger.info(f"Loading collected data into database.")

    await db_load(db_dsn, entries)

    logger.info(f"Data loaded successfully!")
