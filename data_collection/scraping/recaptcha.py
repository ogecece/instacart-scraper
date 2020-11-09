from abc import ABC, abstractmethod

from twocaptcha import TwoCaptcha

from data_collection.settings import TWOCAPTCHA_API_KEY


class BaseRecaptchaSolver(ABC):
    @abstractmethod
    def solve(self, url, sitekey):
        pass


class TwoCaptchaRecaptchaV2Solver(BaseRecaptchaSolver):
    def __init__(self):
        config = {
            "apiKey": TWOCAPTCHA_API_KEY,
            "recaptchaTimeout": 120,
            "pollingInterval": 10,
        }
        self.solver = TwoCaptcha(**config)

    def solve(self, url, sitekey):
        captcha_response = self.solver.recaptcha(url=url, sitekey=sitekey)
        return captcha_response["code"]
