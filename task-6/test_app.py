import mysql.connector
import pytest

import app


class DummyCursor:
    def __init__(self, fixtures):
        self.fixtures = fixtures
        self.last_query = ""

    def execute(self, query):
        self.last_query = query

    def fetchall(self):
        if self.last_query == "SHOW TABLES":
            return [(name,) for name in self.fixtures.keys()]

        if self.last_query.startswith("DESCRIBE "):
            table = self.last_query.split(" ", 1)[1]
            return [(col,) for col in self.fixtures[table]["columns"]]

        if self.last_query.startswith("SELECT * FROM "):
            table = self.last_query.split(" ", 3)[-1]
            return self.fixtures[table]["rows"]

        return []

    def close(self):
        return None


class DummyConnection:
    def __init__(self, fixtures):
        self.cursor_obj = DummyCursor(fixtures)

    def cursor(self):
        return self.cursor_obj

    def close(self):
        return None


@pytest.fixture
def table_fixtures():
    return {
        "users": {
            "columns": ["id", "name"],
            "rows": [(1, "Alice"), (2, "Bob")],
        },
        "orders": {
            "columns": ["id", "product"],
            "rows": [(1, "Widget")],
        },
    }


def test_index_renders_table_data(monkeypatch, table_fixtures):
    def fake_connect(**kwargs):
        return DummyConnection(table_fixtures)

    monkeypatch.setattr(mysql.connector, "connect", fake_connect)

    client = app.app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    body = response.data.decode()
    assert "users" in body
    assert "orders" in body
    assert "Alice" in body
    assert "Widget" in body
