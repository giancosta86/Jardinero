import sys
from logging import getLogger
from os.path import join
from sys import argv

from flask import Flask

from . import PER_USER_HOME_DIRECTORY
from .browser import browser
from .dictionary import DictionaryFacade
from .dictionary.sqlite import SqliteDictionaryFacade
from .extensions import LinguisticModule, LinguisticModuleException, load_linguistic_module

logger = getLogger(__name__)


class JardineroApp(Flask):
    def __init__(self, linguistic_module: LinguisticModule):
        super().__init__(type(self).__name__)
        self.config["SECRET_KEY"] = "hyper-secret!"
        self.register_blueprint(browser)
        self._dictionary_facade = create_dictionary_facade(linguistic_module)

    @property
    def dictionary_facade(self) -> DictionaryFacade:
        return self._dictionary_facade


def create_dictionary_facade(linguistic_module: LinguisticModule) -> DictionaryFacade:

    module_db_directory = join(PER_USER_HOME_DIRECTORY, linguistic_module.name)
    module_db_path = join(module_db_directory, "dictionary.db")

    return SqliteDictionaryFacade(
        wiki_url=linguistic_module.get_wiki_url(),
        sqlite_dictionary_factory=linguistic_module.create_sqlite_dictionary,
        term_extractor=linguistic_module.extract_terms,
        db_file_path=module_db_path,
    )


def create_app_from_sys_args() -> JardineroApp:
    if not argv:
        print("Usage: python info.gianlucacosta.jardinero <linguistic module>")
        sys.exit(1)

    linguistic_module_name = argv[1]

    try:
        linguistic_module = load_linguistic_module(linguistic_module_name)
    except LinguisticModuleException as ex:
        logger.warning("Error while loading module '%s': %r", linguistic_module_name, ex)
        print(ex, file=sys.stderr)
        sys.exit(1)

    return JardineroApp(linguistic_module)


app = create_app_from_sys_args()
