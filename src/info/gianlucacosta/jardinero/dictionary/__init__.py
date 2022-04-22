from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import getLogger
from threading import RLock
from traceback import format_exception
from typing import Optional

from info.gianlucacosta.eos.core.functional import Consumer
from info.gianlucacosta.wikiprism.dictionary import DictionaryViewResult
from info.gianlucacosta.wikiprism.pipeline import PipelineHandle
from info.gianlucacosta.wikiprism.pipeline.protocol import (
    PipelineCanceledException,
    PipelineEndedListener,
    PipelineMessageListener,
)


@dataclass(frozen=True)
class DictionaryStatus:
    status_message: Optional[str]
    pipeline_message: Optional[str]
    error_in_previous_pipeline: Optional[Exception]


@dataclass(frozen=True)
class PipelineStatus:
    handle: Optional[PipelineHandle]
    message: Optional[str]
    error_in_previous: Optional[Exception]


DictionaryStatusListener = Consumer[DictionaryStatus]


class DictionaryFacade(ABC):
    def __init__(self) -> None:
        self._operational_lock = RLock()

        self._pipeline_status = PipelineStatus(handle=None, message=None, error_in_previous=None)

        self._dictionary_status_listeners: list[DictionaryStatusListener] = []

        self._logger = getLogger(type(self).__name__)

    def get_dictionary_status(self) -> DictionaryStatus:
        with self._operational_lock:
            return DictionaryStatus(
                status_message=self._get_status_message(),
                pipeline_message=self._pipeline_status.message,
                error_in_previous_pipeline=self._pipeline_status.error_in_previous,
            )

    @abstractmethod
    def _get_status_message(self) -> Optional[str]:
        pass

    def add_dictionary_status_listener(self, listener: DictionaryStatusListener) -> None:
        with self._operational_lock:
            self._dictionary_status_listeners.append(listener)

    def _notify_pipeline_update(self, pipeline_status: PipelineStatus) -> None:
        with self._operational_lock:
            self._logger.info(
                "Pipeline status updated! Message: '%s'. Error in previous: %r",
                pipeline_status.message,
                pipeline_status.error_in_previous,
            )

            self._pipeline_status = pipeline_status
            dictionary_status = self.get_dictionary_status()

            for listener in self._dictionary_status_listeners:
                listener(dictionary_status)

    def try_to_start_pipeline(self) -> None:
        with self._operational_lock:
            if self._pipeline_status.handle:
                self._logger.warning("A pipeline is already in place!")
                return

            self._logger.info("Now starting the pipeline...")

            pipeline_handle = self._start_pipeline(
                self._on_pipeline_message, self._on_pipeline_ended
            )

            self._notify_pipeline_update(
                PipelineStatus(
                    handle=pipeline_handle,
                    message="Starting the pipeline...",
                    error_in_previous=None,
                )
            )

    @abstractmethod
    def _start_pipeline(
        self, on_message: PipelineMessageListener, on_ended: PipelineEndedListener
    ) -> PipelineHandle:
        pass

    def _on_pipeline_message(self, pipeline_message: str) -> None:
        with self._operational_lock:

            message_originated_pipeline_status = PipelineStatus(
                handle=self._pipeline_status.handle,
                message=pipeline_message,
                error_in_previous=self._pipeline_status.error_in_previous,
            )

            self._notify_pipeline_update(message_originated_pipeline_status)

    def _on_pipeline_ended(self, exception: Optional[Exception]) -> None:
        with self._operational_lock:
            actual_exception = self._get_actual_exception(exception)

            final_pipeline_status = PipelineStatus(
                handle=None,
                message=None,
                error_in_previous=actual_exception,
            )

            self._notify_pipeline_update(final_pipeline_status)

    def _get_actual_exception(self, exception: Optional[Exception]) -> Optional[Exception]:
        match exception:
            case PipelineCanceledException():
                self._logger.info("The pipeline was canceled!")
                return None

            case Exception() as ex:
                traceback = "\n".join(format_exception(ex))
                self._logger.warning(
                    "The pipeline ended with an unexpected exception! %r. Traceback: %s",
                    ex,
                    traceback,
                )
                return ex

            case None:
                self._logger.info("The pipeline has just completed successfully!")
                return None

    def try_to_cancel_pipeline(self) -> None:
        with self._operational_lock:
            if not self._pipeline_status.handle:
                self._logger.warning("There is no active pipeline - cannot cancel!")
                return

            self._logger.info("Sending a cancel request to the pipeline...")
            self._pipeline_status.handle.request_cancel()

    def execute_command(self, command: str) -> DictionaryViewResult:
        with self._operational_lock:
            return self._execute_command(command)

    @abstractmethod
    def _execute_command(self, command: str) -> DictionaryViewResult:
        pass
