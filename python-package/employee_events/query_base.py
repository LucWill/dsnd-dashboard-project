from sqlite3 import connect
from .sql_execution import QueryMixin

class QueryBase(QueryMixin):
    """Base class for querying the employee_events database."""
    
    name = ''

    def names(self):
        """Return an empty list (placeholder method)."""
        return []

    def event_counts(self, id):
        """Retrieve summed positive and negative events by date."""
        query = f'''
            SELECT ev.event_date,
                   SUM(ev.positive_events) AS total_positive,
                   SUM(ev.negative_events) AS total_negative
            FROM {self.name} AS e
            JOIN employee_events AS ev ON e.{self.name}_id = ev.{self.name}_id
            GROUP BY ev.event_date
            ORDER BY ev.event_date
        '''
        return super().pandas_query(query)

    def notes(self, id):
        """Retrieve notes and their dates for a given ID."""
        query = f"""
            SELECT notes.note_date, notes.note
            FROM notes
            JOIN {self.name} ON {self.name}.{self.name}_id = notes.{self.name}_id
            WHERE {self.name}.{self.name}_id = {id}
        """
        return super().pandas_query(query)
