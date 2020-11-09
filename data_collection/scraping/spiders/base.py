from abc import ABC, abstractmethod


class BaseSpider(ABC):
    @abstractmethod
    def crawl(self):
        pass
