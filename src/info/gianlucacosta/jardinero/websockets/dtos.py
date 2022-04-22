from typing import Any

from info.gianlucacosta.wikiprism.dictionary import DictionaryView, DictionaryViewResult

from ..dictionary import DictionaryStatus


def dictionary_status_to_dto(dictionary_status: DictionaryStatus) -> dict[str, Any]:
    return {
        "statusMessage": dictionary_status.status_message,
        "pipelineMessage": dictionary_status.pipeline_message,
        "errorInPreviousPipeline": repr(dictionary_status.error_in_previous_pipeline)
        if dictionary_status.error_in_previous_pipeline
        else None,
    }


def dictionary_view_result_to_dto(
    dictionary_view_result: DictionaryViewResult,
) -> dict[str, Any]:
    match dictionary_view_result:
        case DictionaryView() as dictionary_view:
            return {
                "exception": None,
                "headers": dictionary_view.headers,
                "rows": dictionary_view.rows,
            }
        case Exception() as exception:
            return {
                "exception": repr(exception),
                "headers": None,
                "rows": None,
            }

        case _:
            raise TypeError()
