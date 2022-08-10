import asyncio
import json
import logging
import os
import random
import string
import threading
import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode

import requests

# from .api.comment import Comment
# from .api.hashtag import Hashtag
# from .api.search import Search
# from .api.sound import Sound
# from .api.trending import Trending
# from .api.user import User
# from .api.video import Video
from .browser_utilities.browser import browser
# from .exceptions import *
# from .utilities import LOGGER_NAME

os.environ["no_proxy"] = "127.0.0.1,localhost"

BASE_URL = "https://m.tiktok.com/"
DESKTOP_BASE_URL = "https://www.tiktok.com/"

_thread_lock = threading.Lock()

class Signer:
    _is_context_manager = False
    # user = User
    # search = Search
    # sound = Sound
    # hashtag = Hashtag
    # video = Video
    # trending = Trending
    # comment = Comment
    # logger = logging.getLogger(LOGGER_NAME)

    def __init__(
            self,
            logging_level: int = logging.WARNING,
            request_delay: Optional[int] = None,
            custom_device_id: Optional[str] = None,
            generate_static_device_id: Optional[bool] = False,
            custom_verify_fp: Optional[str] = None,
            use_test_endpoints: Optional[bool] = False,
            proxy: Optional[str] = None,
            executable_path: Optional[str] = None,
            *args,
            **kwargs,
    ):

        with _thread_lock:
            self._initialize(
                request_delay=request_delay,
                custom_device_id=custom_device_id,
                generate_static_device_id=generate_static_device_id,
                custom_verify_fp=custom_verify_fp,
                use_test_endpoints=use_test_endpoints,
                proxy=proxy,
                executable_path=executable_path,
                *args,
                **kwargs,
            )
    
    def _sign(self, full_url, **kwargs):
        self._browser = asyncio.get_event_loop().run_until_complete(
            asyncio.gather(browser.create(**kwargs))
        )[0]
        
        (
                verify_fp,
                device_id,
                signature,
                tt_params,
            ) = asyncio.get_event_loop().run_until_complete(
                asyncio.gather(
                    self._browser.sign_url(
                        full_url, calc_tt_params=None, **kwargs
                    )
                )
            )[
                0
            ]
        return verify_fp, signature, device_id, tt_params

    def _initialize(self, **kwargs):
        # Add classes from the api folder
        # User.parent = self
        # Search.parent = self
        # Sound.parent = self
        # Hashtag.parent = self
        # Video.parent = self
        # Trending.parent = self
        # Comment.parent = self

        # Some Instance Vars
        self._executable_path = kwargs.get("executable_path", None)
        self.cookie_jar = None

        if kwargs.get("custom_did") != None:
            raise Exception("Please use 'custom_device_id' instead of 'custom_did'")
        self._custom_device_id = kwargs.get("custom_device_id", None)
        self._user_agent = "5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"  # TODO: Randomly generate agents
        self._proxy = kwargs.get("proxy", None)
        self._custom_verify_fp = kwargs.get("custom_verify_fp")
        self._signer_url = kwargs.get("external_signer", None)
        self._request_delay = kwargs.get("request_delay", None)
        self._requests_extra_kwargs = kwargs.get("requests_extra_kwargs", {})

        if kwargs.get("use_test_endpoints", False):
            global BASE_URL
            BASE_URL = "https://t.tiktok.com/"

        if kwargs.get("generate_static_device_id", False):
            self._custom_device_id = "".join(
                random.choice(string.digits) for num in range(19)
            )

        if self._signer_url is None:
            self._browser = asyncio.get_event_loop().run_until_complete(
                asyncio.gather(browser.create(**kwargs))
            )[0]

            self._user_agent = self._browser.user_agent

        try:
            self._timezone_name = self._browser.timezone_name
            self._browser_language = self._browser.browser_language
            self._width = self._browser.width
            self._height = self._browser.height
            self._region = self._browser.region
            self._language = self._browser.language
        except Exception as e:
            pass
            # self.logger.exception(
            #     "An error occurred while opening your browser, but it was ignored\n",
            #     "Are you sure you ran python -m playwright install?",
            # )

            self._timezone_name = ""
            self._browser_language = ""
            self._width = "1920"
            self._height = "1080"
            self._region = "US"
            self._language = "en"
            raise e from e

    def shutdown(self) -> None:
        with _thread_lock:
            # self.logger.debug("Shutting down Playwright")
            asyncio.get_event_loop().run_until_complete(self._browser._clean_up())

    def __enter__(self):
        with _thread_lock:
            self._is_context_manager = True
            return self

    def __exit__(self, type, value, traceback):
        self.shutdown()
