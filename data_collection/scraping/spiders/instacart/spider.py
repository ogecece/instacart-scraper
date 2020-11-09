import logging
from asyncio import gather
from urllib.parse import urljoin

from aiohttp import ClientSession

from data_collection.scraping.recaptcha import (
    TwoCaptchaRecaptchaV2Solver as RecaptchaSolver,
)
from data_collection.scraping.spiders.base import BaseSpider
from data_collection.settings import INSTACART_LOGIN, INSTACART_PASSWORD

from .pages import HomePage, SelectStorePage, ShelfPage, StorePage

logger = logging.getLogger(__name__)


class InstacartSpider(BaseSpider):
    HOME_URL = "https://www.instacart.com"
    LOGIN_URL = "https://www.instacart.com/v3/dynamic_data/authenticate/login"
    SELECT_STORE_URL = "https://www.instacart.com/store"
    STORE_URL = "https://www.instacart.com/v3/containers/{slug}/storefront"

    async def crawl(self):
        logger.info("Starting Instacart crawl.")

        async with ClientSession() as session:
            auth_token, captcha_code = await self.parse_home(session)
            logger.info("Homepage parsed.")

            logger.info("Logging in...")
            await self.login(session, auth_token, captcha_code)

            store_metadata = await self.select_store(session)
            logger.info(f"Store selected: {store_metadata['store_name']}.")

            shelves_metadata = await self.parse_store(session, store_metadata)
            logger.info(f"Shelves metadata collected.")

            shelves_items = [
                c async for c in self.parse_shelves(session, shelves_metadata)
            ]
            logger.info(f"Shelves items collected.")

        shelves = [
            {"shelf_name": meta["name"], "shelf_items": items}
            for meta, items in zip(shelves_metadata, shelves_items)
        ]
        output = {
            "store_name": store_metadata["store_name"],
            "store_logo_url": store_metadata["store_logo_url"],
            "shelves": shelves,
        }

        logger.info("Finishing Instacart crawl.")

        return output

    async def parse_home(self, session):
        async with session.get(self.HOME_URL) as res:
            homepage = HomePage.from_html(await res.text())
            auth_token = homepage.auth_token()
            sitekey = homepage.sitekey()

            recaptcha_solver = RecaptchaSolver()
            captcha_code = recaptcha_solver.solve(res.url, sitekey)

        return auth_token, captcha_code

    async def login(self, session, auth_token, captcha_code):
        login_formdata = {
            "address": None,
            "authenticity_token": auth_token,
            "captcha": captcha_code,
            "email": INSTACART_LOGIN,
            "grant_type": "password",
            "password": INSTACART_PASSWORD,
            "scope": "",
            "signup_v3_endpoints_web": None,
        }
        await session.post(self.LOGIN_URL, json=login_formdata)

    async def select_store(self, session):
        async with session.get(self.SELECT_STORE_URL) as res:
            select_store_page = SelectStorePage.from_html(await res.text())
            store_url = select_store_page.store_url()

        return store_url

    async def parse_store(self, session, store_metadata):
        store_slug = store_metadata["store_slug"]
        async with session.get(self.STORE_URL.format(slug=store_slug)) as res:
            store_page = StorePage.from_json(await res.text())
            shelves_metadata = store_page.shelves()

        return shelves_metadata

    async def parse_shelves(self, session, shelves_metadata):
        shelves_requests = [
            session.get(urljoin(self.HOME_URL, shelf["href"]))
            for shelf in shelves_metadata
        ]
        shelves_responses = await gather(*shelves_requests)

        for shelf_response in shelves_responses:
            shelf_page = ShelfPage.from_json(await shelf_response.text())
            items_names = shelf_page.items_names()
            yield items_names
