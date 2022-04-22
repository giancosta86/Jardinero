import bz2
from multiprocessing import Pool
from os import unlink
from sqlite3 import Connection
from typing import Optional, TextIO, TypeVar

from info.gianlucacosta.eos.core.multiprocessing.pool import AnyProcessPool
from info.gianlucacosta.wikiprism.dictionary.sqlite import SqliteDictionary
from info.gianlucacosta.wikiprism.pipeline.pool import TermExtractor
from info.gianlucacosta.wikiprism.pipeline.protocol import (
    PipelineCanceledException,
    PipelineEndedListener,
    PipelineMessageListener,
    WikiFile,
)
from info.gianlucacosta.wikiprism.pipeline.sqlite import (
    SqliteDictionaryFactory,
    SqlitePipelineStrategy,
)

from ...utils.downloads import download_file_as_temp

TTerm = TypeVar("TTerm")


class DownloadingSqlitePipelineStrategy(SqlitePipelineStrategy[TTerm]):
    def __init__(
        self,
        target_db_path: str,
        dictionary_factory: SqliteDictionaryFactory[TTerm],
        wiki_url: str,
        term_extractor: TermExtractor[TTerm],
        on_message: PipelineMessageListener,
        on_ended: PipelineEndedListener,
    ) -> None:
        super().__init__(target_db_path)
        self._dictionary_factory = dictionary_factory
        self._wiki_url = wiki_url
        self._term_extractor = term_extractor
        self._on_message = on_message
        self._on_ended = on_ended

        self._temp_wiki_path: Optional[str] = None
        self._temp_wiki_stream: Optional[TextIO] = None

    def create_pool(self) -> AnyProcessPool:
        return Pool()

    def create_dictionary_from_connection(self, connection: Connection) -> SqliteDictionary[TTerm]:
        return self._dictionary_factory(connection)

    def get_wiki_file(self) -> WikiFile:
        return self._download_wiki_to_temp_file()

    def _download_wiki_to_temp_file(self) -> TextIO:
        self._logger.info("Downloading wiki from %s...", self._wiki_url)
        self._on_message("Downloading wiki...")

        self._temp_wiki_path = download_file_as_temp(
            url=self._wiki_url, continuation_provider=lambda: self._never_canceled
        )

        if not self._temp_wiki_path:
            self._logger.warning("Wiki download canceled!")
            raise PipelineCanceledException()

        self._on_message("Wiki downloaded!")

        self._temp_wiki_stream = bz2.open(self._temp_wiki_path, mode="rt", encoding="utf-8")
        return self._temp_wiki_stream

    def get_term_extractor(self) -> TermExtractor[TTerm]:
        return self._term_extractor

    def perform_last_successful_steps(self) -> None:
        try:
            if self._temp_wiki_stream:
                self._logger.info("Now closing the wiki stream...")
                self._temp_wiki_stream.close()

            if self._temp_wiki_path:
                self._logger.info("Now deleting the downloaded wiki...")
                unlink(self._temp_wiki_path)
                self._logger.info("Wiki file deleted!")
        finally:
            super().perform_last_successful_steps()

    def on_message(self, message: str) -> None:
        self._on_message(message)

    def on_ended(self, exception: Optional[Exception]) -> None:
        super().on_ended(exception)
        self._on_ended(exception)
