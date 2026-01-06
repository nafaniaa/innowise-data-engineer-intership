from app.db.sql_executor import SQLExecutor


class AnalyticsService:
    def __init__(self, executor: SQLExecutor):
        self.executor = executor

    def rooms_with_students_count(self):
        return self.executor.execute_select(
            "sql_queries/analytics/rooms_with_students_count.sql"
        )

    def top_5_rooms_with_smallest_avg_age(self):
        return self.executor.execute_select(
            "sql_queries/analytics/top_5_rooms_with_smallest_avg_age.sql"
        )

    def top_5_rooms_with_max_age_diff(self):
        return self.executor.execute_select(
            "sql_queries/analytics/top_5_rooms_with_max_age_diff.sql"
        )

    def rooms_with_mixed_sex(self):
        return self.executor.execute_select(
            "sql_queries/analytics/rooms_with_mixed_sex.sql"
        )
