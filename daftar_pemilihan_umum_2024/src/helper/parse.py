from src.exceptions.exceptions import ErrorParseData

from parsel import Selector
import requests
import aiohttp

class Parse:

    def __init__() -> None:
        pass


    @staticmethod
    async def selector(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = requests.get(url)
                if response.status_code == 200:
                    selector = Selector(text=response.text)
                    return selector
                else:
                    raise ErrorParseData()

    
    @staticmethod
    async def get_status_code(url):
        response = requests.get(url)
        if response.status_code == 200:
            return 200
        else:
            return response.status_code