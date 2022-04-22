from sqlite3 import connect
from typing import Generic, Optional, TypeVar

from info.gianlucacosta.eos.core.io.files import get_modification_datetime
from info.gianlucacosta.wikiprism.pipeline import PipelineHandle, run_extraction_pipeline
from info.gianlucacosta.wikiprism.pipeline.pool import TermExtractor
from info.gianlucacosta.wikiprism.pipeline.protocol import (
    PipelineEndedListener,
    PipelineMessageListener,
)
from info.gianlucacosta.wikiprism.pipeline.sqlite import SqliteDictionaryFactory

from .. import DictionaryFacade, DictionaryViewResult
from .strategy import DownloadingSqlitePipelineStrategy

TTerm = TypeVar("TTerm")


class SqliteDictionaryFacade(Generic[TTerm], DictionaryFacade):
    def __init__(
        self,
        wiki_url: str,
        sqlite_dictionary_factory: SqliteDictionaryFactory[TTerm],
        term_extractor: TermExtractor[TTerm],
        db_file_path: str,
    ) -> None:
        super().__init__()
        self._wiki_url = wiki_url
        self._sqlite_dictionary_factory = sqlite_dictionary_factory
        self._term_extractor = term_extractor
        self._db_file_path = db_file_path

    def _start_pipeline(
        self, on_message: PipelineMessageListener, on_ended: PipelineEndedListener
    ) -> PipelineHandle:
        pipeline_strategy = DownloadingSqlitePipelineStrategy(
            dictionary_factory=self._sqlite_dictionary_factory,
            wiki_url=self._wiki_url,
            target_db_path=self._db_file_path,
            term_extractor=self._term_extractor,
            on_message=on_message,
            on_ended=on_ended,
        )
        return run_extraction_pipeline(pipeline_strategy)

    def _get_status_message(self) -> Optional[str]:
        db_modification_datetime = get_modification_datetime(self._db_file_path)

        return (
            f"Dictionary updated on: {db_modification_datetime.ctime()}"
            if db_modification_datetime
            else None
        )

    def _execute_command(self, command: str) -> DictionaryViewResult:
        with self._sqlite_dictionary_factory(connect(self._db_file_path)) as dictionary:
            return dictionary.execute_command(command)
