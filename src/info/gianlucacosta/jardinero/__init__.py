from logging import ERROR, WARNING, basicConfig
from os.path import join
from pathlib import Path

DEV_MODE = __debug__

PORT = 7000

APP_URL = f"http://localhost:{PORT}/"

FRONTEND_SERVER_URL = "http://localhost:8080"

PER_USER_HOME_DIRECTORY = join(Path.home(), ".jardinero")


basicConfig(
    level=WARNING if DEV_MODE else ERROR,
    encoding="utf-8",
    format="%(asctime)s <%(name)s> %(message)s",
)
