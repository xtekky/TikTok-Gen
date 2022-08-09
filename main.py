import requests
import json
import threading
import random
import re

proxy = '2kicnOO3:neMghWGg9N@nprx.rainproxy.io:5000'
proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
}

class Gen:
    def __init__(self):
        self.__client = requests.Session()
    
    def __base_headers(self, addon: json = {}) -> json:

        __base_headers = {
            'authority': 'www.tiktok.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'cookie': str(self.__cookie_to_str(self.__client.cookies.get_dict())),
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        
        __base_headers.update(addon)
        
        return __base_headers
    
    def __cookie_to_str(self, cookies) -> str:
        cookies_str = ""
        for i in cookies.items():
            cookies_str = cookies_str + i[0] + "=" + i[1] + "; "
        return cookies_str[: len(cookies_str) - 2]

    def __get_wid(self) -> str:

        __html = self.__client.get(
            url = 'https://www.tiktok.com/signup/phone-or-email/email',
            headers = self.__base_headers()
        )
        return str(
            re.findall(r'wid":"(\d*)"', __html.text)[0]
        )
    
    def main(self):
        __wid = self.__get_wid()
        print()


Gen().main()