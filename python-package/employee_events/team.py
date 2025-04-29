from .query_base import QueryBase


class Team(QueryBase):
    """Represents the team table in the database."""

    name = "team"

    def names(self):
        """Retrieve team names and their IDs."""
        sql_query = """
            SELECT team_name, team_id
            FROM team;
        """
        return self.query(sql_query)

    def username(self, id: str):
        """Retrieve a team name by team ID."""
        sql_query = f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """
        return self.query(sql_query)

    def model_data(self, id: str):
        """Retrieve event data for all employees of a team
            as a pandas DataFrame."""
        sql_query = f"""
            SELECT positive_events, negative_events
            FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                GROUP BY employee_id
            )
        """
        return self.pandas_query(sql_query)
