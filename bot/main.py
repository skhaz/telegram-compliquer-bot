import os
import http

import requests

from flask import Flask, request
from werkzeug.wrappers import Response

from telegram import Bot, Update, ParseMode
from telegram.ext import Dispatcher, Filters, CommandHandler, CallbackContext

app = Flask(__name__)

session = requests.Session()


def run(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip("/run")
    if not text:
        return

    payload = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "execute",
        "params": {"source": text},
    }

    response = session.post(os.environ["JSON_RPC"], json=payload)
    response.raise_for_status()
    result = response.json().get("result")

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
