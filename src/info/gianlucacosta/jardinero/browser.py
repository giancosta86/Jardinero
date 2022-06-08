from logging import getLogger
from os.path import dirname, join

from flask import Blueprint, redirect, send_file
from werkzeug import Response

from . import DEV_MODE, FRONTEND_SERVER_URL, PORT

logger = getLogger(__name__)

browser = Blueprint("browser", __name__)


@browser.route("/")
def index_handler() -> Response:
    return static_handler("index.html")


@browser.route("/<path:path>")
def static_handler(path: str) -> Response:
    if DEV_MODE:
        frontend_url = f"{FRONTEND_SERVER_URL}/{path}?backend-port={PORT}"
        logger.info(
            "As we are in dev mode, I'm redirecting to the frontend server! -> %s", frontend_url
        )
        return redirect(frontend_url)

    static_file_path = join(dirname(__file__), "static", path)
    logger.info("Returning a static file, as expected -> %s", static_file_path)
    return send_file(static_file_path)
