import requests
import json
import time
import threading
import random
import re

from urllib.parse import *
from utils.signature import Signature
from utils.bogus import XBogus

class Gen:
    def __init__(self):
        self.__client = requests.Session()
        self.__wid = None
        
    def __base_params(self, addon: json = {}):
        
        __base_params = {
            "aid"             : 1459,
            "app_language"    : "en",
            "app_name"        : "tiktok_web",
            "battery_info"    : 1,
            "browser_language": "en",
            "browser_name"    : "Mozilla",
            "browser_online"  : True,
            "browser_platform": "Win32",
            "browser_version" : "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "channel"         : "tiktok_web",
            "cookie_enabled"  : True,
            "device_id"       : self.__wid,
            "device_platform" : "web_pc",
            "focus_state"     : True,
            "history_len"     : "2",
            "is_fullscreen"   : False,
            "is_page_visible" : True,
            "os"              : "windows",
            "region"          : "FR",
            "screen_height"   : 1080,
            "screen_width"    : 1920,
            "tz_name"         : "Europe/Paris",
            "webcast_language": "en",
            "X-Bogus"         : '%s' % XBogus.get_value(),
            "_signature"      : '%s' % Signature.get_value()
        }
        
        __base_params.update(addon)
        
        return urlencode(__base_params)
    
    def __base_headers(self, addon: json = {}) -> json:

        __base_headers = {
            'authority'         : 'www.tiktok.com',
            'accept'            : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language'   : 'en',
            'cache-control'     : 'no-cache',
            'pragma'            : 'no-cache',
            'sec-ch-ua'         : '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile'  : '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest'    : 'document',
            'sec-fetch-mode'    : 'navigate',
            'sec-fetch-site'    : 'none',
            'sec-fetch-user'    : '?1',
            'cookie'            : str(
                    self.__cookie_to_str(
                    self.__client.cookies.get_dict()
                )
            ),
            'upgrade-insecure-requests': '1',
            'user-agent'               : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        
        __base_headers.update(addon)
        
        return __base_headers
    
    def __cache_token(self, __wid: str) -> str:
        return '{%22_type_%22:%22default%22%2C%22user_unique_id%22:%22' + __wid + '%22%2C%22timestamp%22:' + str(int(time.time())) + '}'
    
    def __cookie_to_str(self, cookies: json) -> str:
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
        
    def __account_info(self):
        __response = requests.get(
            url = (
                'https://'
                + 'www.tiktok.com'
                + '/passport/web/account/info/?'
                + self.__base_params()
            ),
            headers = self.__base_headers()
        )
        
        return __response.json()
    
    def main(self):
        self.__wid = self.__get_wid()
        self.__client.cookies.set(
            "__tea_cache_tokens_1988", self.__cache_token(self.__wid)
        )
        self.__account_info = self.__account_info()
        print(self.__account_info)

# Gen().main() 
if __name__ == '__main__':
    # Gen().main()
    # url = 'https://www.tiktok.com/passport/web/account/info/?aid=1459&app_language=en&app_name=tiktok_web&battery_info=1&browser_language=en&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F103.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id=7129986638319289862&device_platform=web_pc&focus_state=true&from_page=&history_len=2&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=&referer=&region=FR&screen_height=1080&screen_width=1920&tz_name=Europe%2FParis&webcast_language=en&msToken=&X-Bogus=DFSzswVOm30ANGA/S6RswGXyYJWC&_signature=_02B4Z6wo00001QzTIbAAAIDAL3IPHGpxIqEM0yUAACHI1c'
    # print(json.dumps(dict(parse_qsl(urlsplit(url).query)), indent=4))
    
    
    from utils.signer.signature import Signer

    with Signer() as signer:
        verify_fp, signature, device_id, tt_params = signer._sign('https://us.tiktok.com/api/commit/follow/user/?aid=1988&app_language=zh-Hant-TW&app_name=tiktok_web&battery_info=0.58&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F97.0.4692.99%20Safari%2F537.36&channel=tiktok_web&channel_id=0&cookie_enabled=true&device_id=7044877592931976705&device_platform=web_pc&focus_state=true&from=18&fromWeb=1&from_page=user&from_pre=0&history_len=2&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=&referer=&region=US&screen_height=900&screen_width=1440&sec_user_id=MS4wLjABAAAAYQIn0ghGQeUMmuqngrxATRDvKvq8dksgQBjXfrOdFo6wdO3DGbciDey2TfJE6EAR&type=1&tz_name=America%2FChicago&user_id=7035930273985479685&webcast_language=zh-Hant-TW&msToken=9ZVRfvLh5KCA9fRwcMTx5ysMVMj7H45hx2NXcHnbY9e1jcESeY2W74Pg3yyBDNFWV8FiPTkZKizt9BhfdgLhahVygTko7rZsISzU8zN408oycsxLlALrDRHd5mW-jBPFsda-dQ==&X-Bogus=DFSzs3fLzhXANxVYSLIiPRKeej0y&_signature=_02B4Z6wo00001j7htJQAAIDDQG3qaCLmgBY-4dgAAO5X40')
        print(signature)
        print(device_id)
        print(verify_fp)
        print(tt_params)

            # # Prints the author's username of the trending video.
            # print(trending_video.author.username)