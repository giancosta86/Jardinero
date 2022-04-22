from logging import getLogger
from sqlite3 import DatabaseError

from info.gianlucacosta.eos.core.db.sqlite import create_memory_db

logger = getLogger(__name__)


class TestMultiInsertions:
    def test_without_errors(self):
        with create_memory_db() as connection:
            connection.executescript(
                """
                CREATE TABLE bears (
                    name NOT NULL,
                    PRIMARY KEY (name)
                )
                """
            )

            bears = [("Yogi",), ("Bubu",)]

            try:
                connection.executemany("INSERT INTO bears VALUES (?)", bears)
            except DatabaseError as ex:
                logger.info(ex)

            cursor = connection.execute("SELECT COUNT(*) FROM bears")

            result = cursor.fetchone()

            assert result == (2,)

    class TestWithErrors:
        def test_when_using_insert(self):
            with create_memory_db() as connection:
                connection.executescript(
                    """
                    CREATE TABLE bears (
                        name NOT NULL,
                        PRIMARY KEY (name)
                    )
                    """
                )

                bears = [("Yogi",), (None,), ("Bubu",)]

                try:
                    connection.executemany("INSERT INTO bears VALUES (?)", bears)
                except DatabaseError:
                    pass

                cursor = connection.execute("SELECT COUNT(*) FROM bears")

                result = cursor.fetchone()

                assert result == (1,)

        def test_when_using_insert_or_ignore(self):
            with create_memory_db() as connection:
                connection.executescript(
                    """
                    CREATE TABLE bears (
                        name NOT NULL,
                        PRIMARY KEY (name)
                    )
                    """
                )

                bears = [("Yogi",), (None,), ("Bubu",)]

                try:
                    connection.executemany("INSERT OR IGNORE INTO bears VALUES (?)", bears)
                except DatabaseError:
                    pass

                cursor = connection.execute("SELECT COUNT(*) FROM bears")

                result = cursor.fetchone()

                assert result == (2,)


def test_single_insertions_with_errors():
    with create_memory_db() as connection:
        connection.executescript(
            """
            CREATE TABLE bears (
                name NOT NULL,
                PRIMARY KEY (name)
            )
            """
        )

        bears = [("Yogi",), (None,), ("Bubu",)]

        for bear in bears:
            try:
                connection.execute("INSERT INTO bears VALUES (?)", bear)
            except DatabaseError:
                pass

        cursor = connection.execute("SELECT COUNT(*) FROM bears")

        result = cursor.fetchone()

        assert result == (2,)
