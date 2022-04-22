from dataclasses import dataclass
from importlib import import_module
from typing import Any

from info.gianlucacosta.eos.core.functional import AnyCallable, Producer
from info.gianlucacosta.wikiprism.pipeline.protocol import TermExtractor
from info.gianlucacosta.wikiprism.pipeline.sqlite import SqliteDictionaryFactory


@dataclass
class LinguisticModule:
    name: str
    get_wiki_url: Producer[str]
    extract_terms: TermExtractor[Any]
    create_sqlite_dictionary: SqliteDictionaryFactory[Any]


class LinguisticModuleException(Exception):
    pass


def load_linguistic_module(module_name: str) -> LinguisticModule:
    def load_module() -> Any:
        try:
            return import_module(module_name)
        except ImportError as ex:
            raise LinguisticModuleException(
                "The requested linguistic module:\n\n"
                f"\t{module_name}\n\n"
                "is not available: have you installed it into your current Python "
                "distribution?\n\n"
                "For example, you might want to run:\n\n"
                f"\tpip install {module_name}"
            ) from ex

    def load_function_from_module(source_module: Any, function_name: str) -> AnyCallable:
        attribute = getattr(source_module, function_name, None)

        if not callable(attribute):
            raise LinguisticModuleException(
                f"Module {module_name} does not have a callable '{function_name}' attribute!"
            )

        return attribute

    module = load_module()

    return LinguisticModule(
        name=module_name,
        get_wiki_url=load_function_from_module(module, "get_wiki_url"),
        extract_terms=load_function_from_module(module, "extract_terms"),
        create_sqlite_dictionary=load_function_from_module(module, "create_sqlite_dictionary"),
    )
