from logging import getLogger
from typing import Any

from flask_socketio import SocketIO, emit

from .. import DEV_MODE
from ..app import app
from .dtos import dictionary_status_to_dto, dictionary_view_result_to_dto
from .status import try_to_start_status_thread

logger = getLogger(__name__)


def create_socket_options() -> dict[str, Any]:
    socket_options = {}

    if DEV_MODE:
        socket_options["cors_allowed_origins"] = "*"

    return socket_options


socketio = SocketIO(app, **create_socket_options())


@socketio.event
def connect() -> None:
    try_to_start_status_thread(socketio)


@socketio.event
def dictionary_status_request() -> None:
    logger.info("I got a 'dictionary_status_request' message from client! ^__^")
    send_dictionary_status_response()


def send_dictionary_status_response() -> None:
    dictionary_status = app.dictionary_facade.get_dictionary_status()

    response_dto = dictionary_status_to_dto(dictionary_status)

    logger.info("Now sending a 'dictionary_status_response' message! ^__^")

    emit("dictionary_status_response", response_dto)


@socketio.event
def start_pipeline() -> None:
    logger.info("I got a 'start_pipeline' message from client! ^__^")
    app.dictionary_facade.try_to_start_pipeline()
    send_dictionary_status_response()


@socketio.event
def cancel_pipeline() -> None:
    logger.info("I got a 'cancel_pipeline' message from client! ^__^")
    app.dictionary_facade.try_to_cancel_pipeline()


@socketio.event
def run_command(command: str) -> None:
    logger.info("I got a 'run_command' message! ^__^\n\t%s", command)

    dictionary_view_result = app.dictionary_facade.execute_command(command)

    response_dto = dictionary_view_result_to_dto(dictionary_view_result)

    emit("command_response", response_dto)
