import os
import http
import functools

import requests

from flask import Flask, request
from werkzeug.wrappers import Response

from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

app = Flask(__name__)


class JSONRPC:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def _make_payload(self, method, params):
        return {"id": 0, "jsonrpc": "2.0", "method": method, "params": params}

    def dispatch(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            payload = self._make_payload(func.__name__, kwargs.copy())
            response = self.session.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()

        return wrapper


rpc = JSONRPC(url=os.environ["JSON_RPC"])


@rpc.dispatch
def execute(source: str) -> dict:
    pass


def run(update: Update, context: CallbackContext) -> None:
    message = update.message
    text = message.text.strip("/run")
    if not text:
        return

    user = message.from_user or message.chat_id

    result = execute(source=text).get("result")

    if result:
        message = update.message.reply_to_message or update.message
        message.reply_text(result)


bot = Bot(token=os.environ["TOKEN"])

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
dispatcher.add_handler(CommandHandler("run", run))


@app.route("/", methods=["POST"])
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
