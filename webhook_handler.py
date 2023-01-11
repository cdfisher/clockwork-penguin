"""webhook_handler.py
Class-based solution for handling the sending of messages and images
to Discord via webhooks.

Thanks to Bals2oo8 for giving me a hand with getting
file sending working.
"""
import json
import requests
import datetime

from config import *
from logging_ import log_message

if TEST_MODE:
    wh_url = TEST_WEBHOOK
else:
    wh_url = WEBHOOK


class WebhookHandler:
    _files = {}
    webhook_data = {}

    def __int__(self):
        self._files = {}
        self.webhook_data = {}

    def add_file(self, file: bytes, filename: str) -> None:
        self._files[f"_{filename}"] = (filename, file)

    def config_webhook(self, content: str, username: str) -> None:
        self.webhook_data["content"] = content
        self.webhook_data["username"] = username

    def make_post_request(self, url: str, data: dict, _files: dict) -> requests.post:
        if not bool(self._files):
            return requests.post(url, json=data)

        self._files["payload_json"] = (None, json.dumps(data))
        return requests.post(url, files=self._files)

    def send_message(self, msg: str, name=BOT_NAME, avatar=AVATAR_URL):
        self.config_webhook(msg, name)
        self.webhook_data["avatar_url"] = avatar
        response = self.make_post_request(wh_url, self.webhook_data, self._files)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log_message(err)
        else:
            now = datetime.datetime.now()
            timestamp = now.strftime('%d %b %Y - %H:%M:%S ')
            log_message(f'Text payload delivered with code {response.status_code} '
                        f'at {timestamp}')
            self.webhook_data = {}
            self._files = {}

    def send_file(self, msg: str, filename: str, name=BOT_NAME, avatar=AVATAR_URL):
        self.config_webhook(msg, name)
        self.webhook_data["avatar_url"] = avatar
        self.add_file(open(filename, 'rb'), filename)
        response = self.make_post_request(wh_url, self.webhook_data, self._files)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log_message(err)
        else:
            now = datetime.datetime.now()
            timestamp = now.strftime('%d %b %Y - %H:%M:%S ')
            log_message(f'File payload delivered with code {response.status_code}'
                        f' at {timestamp}')
        self.webhook_data = {}
        self._files = {}
