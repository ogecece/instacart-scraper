import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

import asyncio
import logging

from data_collection.utils import setup_logging
from data_collection.workflow.pipelines import instacart_shelves

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    logger.info("Execution started.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(instacart_shelves())
    loop.close()

    logger.info("Execution finished.")


if __name__ == "__main__":
    main()
