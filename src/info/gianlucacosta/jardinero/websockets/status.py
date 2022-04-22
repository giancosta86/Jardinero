from logging import getLogger
from typing import Optional

from flask_socketio import SocketIO
from info.gianlucacosta.eos.core.threading.atomic import Atomic

from ..app import app
from ..dictionary import DictionaryStatus
from .dtos import dictionary_status_to_dto

logger = getLogger(__name__)

SLEEP_SECONDS = 1


background_thread_registered = Atomic[bool](False)


def try_to_start_status_thread(socketio: SocketIO) -> None:
    if background_thread_registered.get_then_set(True):
        return

    new_dictionary_status = Atomic[Optional[DictionaryStatus]](None)

    def on_dictionary_status_updated(dictionary_status: DictionaryStatus) -> None:
        new_dictionary_status.set(dictionary_status)

    app.dictionary_facade.add_dictionary_status_listener(on_dictionary_status_updated)

    def dictionary_status_thread() -> None:
        logger.info("Background thread started!")

        while True:
            dictionary_status_to_broadcast = new_dictionary_status.get_then_set(None)
            if dictionary_status_to_broadcast:
                logger.info("Updates found by the background thread!")

                dictionary_status_message = dictionary_status_to_dto(
                    dictionary_status_to_broadcast
                )

                with app.app_context():
                    socketio.emit(
                        "dictionary_status_response",
                        dictionary_status_message,
                        broadcast=True,
                        namespace="/",
                    )

            socketio.sleep(SLEEP_SECONDS)

    logger.info("Now starting the background thread...")
    socketio.start_background_task(dictionary_status_thread)
    logger.info("Background thread registered!")
