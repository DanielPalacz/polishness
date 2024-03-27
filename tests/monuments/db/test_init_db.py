from polishness.api.monuments.tools.constants import DEF_SQLLITE_SCHEMA
from polishness.api.monuments.tools.db_setup import init_db


def test_initDb_defaultRun(monkeypatch, t_file):
    store_for_script_calls = []

    class DbConnFake:
        store = []
        called = False

        @staticmethod
        def executescript(script: str):
            store_for_script_calls.append(script)

    def get_db_connection_fake(location: str) -> DbConnFake:
        return DbConnFake()

    monkeypatch.setattr("polishness.api.monuments.tools.db_setup.get_db_connection", get_db_connection_fake)
    db_initiation_status = init_db(None, t_file)
    assert db_initiation_status is None
    assert [DEF_SQLLITE_SCHEMA] == store_for_script_calls
