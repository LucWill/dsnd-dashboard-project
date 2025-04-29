import pytest
from pathlib import Path
from sqlite3 import connect

# Absolute path to the project root
project_root = Path(__file__).parent.parent


@pytest.fixture
def db_path():
    """Return a Path object to the employee_events.db file."""
    return (
            project_root
            / "python-package"
            / "employee_events"
            / "employee_events.db"
        )


def test_db_exists(db_path):
    """Check that the database file exists."""
    assert db_path.is_file()


@pytest.fixture
def db_conn(db_path):
    """Provide a sqlite3 connection to the database."""
    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    """Return a list of table names in the database."""
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [x[0] for x in name_tuples]


def test_employee_table_exists(table_names):
    """Check that the 'employee' table exists."""
    assert "employee" in table_names


def test_team_table_exists(table_names):
    """Check that the 'team' table exists."""
    assert "team" in table_names


def test_employee_events_table_exists(table_names):
    """Check that the 'employee_events' table exists."""
    assert "employee_events" in table_names
