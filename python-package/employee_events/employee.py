from .query_base import QueryBase
from .sql_execution import QueryMixin, query

class Employee(QueryBase):
    """Represents the employee table in the database."""
    
    name = "employee"

    def names(self):
        """Retrieve full names and IDs of all employees."""
        sql_query = """
            SELECT first_name || ' ' || last_name AS full_name,
                   employee_id
            FROM employee;
        """
        return self.query(sql_query)

    def username(self, id: int):
        """Retrieve full name of an employee by ID."""
        sql_query = f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {id}
        """
        return self.query(sql_query)

    def model_data(self, id: int):
        """Retrieve aggregated event data for a given employee as a pandas DataFrame."""
        sql_query = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(sql_query)