from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Path to the employee_events database
db_path = Path(__file__).parent / 'employee_events.db'


class QueryMixin:
    """Provides methods for executing SQL queries."""

    def pandas_query(self, sql_query: str):
        """Execute an SQL query and return the result as a pandas DataFrame."""
        con = connect(db_path)
        df = pd.read_sql_query(sql_query, con)
        con.close()
        return df

    def query(self, sql_query: str):
        """Execute an SQL query and return the result as a list of tuples."""
        con = connect(db_path)
        cursor = con.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        con.close()
        return results


def query(func):
    """Decorator to execute a generated SQL query and
        return a list of tuples."""
    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result

    return run_query
