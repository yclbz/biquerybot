from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from .db import execute_query

class QueryRunner:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute_safe_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return the results as a list of dictionaries.
        Only SELECT queries are allowed for security.
        """
        # Basic SQL injection prevention
        query = query.strip()
        if not query.lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed")

        # Execute the query
        try:
            results = await execute_query(self.session, query)
            return [dict(row) for row in results]
        except Exception as e:
            raise ValueError(f"Error executing query: {str(e)}")

    def validate_query(self, query: str) -> bool:
        """
        Validate if the query is safe to execute.
        """
        query_lower = query.lower()
        
        # Check for dangerous keywords
        dangerous_keywords = [
            "delete", "drop", "truncate", "insert", "update",
            "alter", "create", "replace", "exec", "execute"
        ]
        
        return (
            query_lower.startswith("select") and
            not any(keyword in query_lower for keyword in dangerous_keywords)
        ) 