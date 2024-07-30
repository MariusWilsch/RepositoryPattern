# src_refactoring/base_repository.py
from abc import ABC
from typing import Any, List, Dict, Union
from enum import Enum
from supabase import create_client, Client
import os


class SupabaseSingleton:
    _instance = None

    @classmethod
    def get_instance(cls) -> Client:
        if cls._instance is None:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
            if not supabase_url or not supabase_key:
                raise ValueError(
                    "Supabase URL and KEY must be set in environment variables"
                )
            cls._instance = create_client(supabase_url, supabase_key)
        return cls._instance


class FilterOperator(Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    LIKE = "like"
    ILIKE = "ilike"
    IS = "is"
    IN = "in"


class DatabaseError(Exception):
    """Exception raised for errors related to database operations."""

    def __init__(self, message="Error occurred during database operation"):
        super().__init__(message)


class BaseRepository(ABC):
    def __init__(self, table_name: str, primary_key: str, logger):
        self.table_name = table_name
        self.primary_key = primary_key
        self.supabase = SupabaseSingleton.get_instance()
        self.logger = logger

    def _execute_query(self, operation: str, query):
        try:
            result = query.execute()
            self.logger.info(
                f"--> {operation.capitalize()} operation successful on {self.table_name}"
            )
            return result.data
        except Exception as e:
            self.logger.error(
                f"Error in {operation} operation on {self.table_name}: {str(e)}"
            )
            raise DatabaseError(f"Failed to {operation} record: {str(e)}")

    def read(self, value: Any = None, column: str = None) -> List[Dict[str, Any]]:
        """Read records from the database.

        Args:
            value (Any, optional): The value to filter by. Defaults to None.
            column (str, optional): The column to filter on. Defaults to None (uses primary key).

        Returns:
            List[Dict[str, Any]]: List of records matching the filter conditions.
        """
        column = column or self.primary_key
        query = self.supabase.table(self.table_name).select("*").eq(column, value)
        return self._execute_query("read", query)

    def update(
        self, value: Any, data: Dict[str, Any], column: str = None
    ) -> List[Dict[str, Any]]:
        """Update records in the database.

        Args:
            value (Any): The value to filter by.
            data (Dict[str, Any]): The data to update.
            column (str, optional): The column to filter on. Defaults to None (uses primary key).

        Returns:
            List[Dict[str, Any]]: List of updated records.
        """
        column = column or self.primary_key
        query = self.supabase.table(self.table_name).update(data).eq(column, value)
        return self._execute_query("update", query)

    def delete(self, value: Any, column: str = None) -> List[Dict[str, Any]]:
        """Delete records from the database.

        Args:
            value (Any): The value to filter by.
            column (str, optional): The column to filter on. Defaults to None (uses primary key).

        Returns:
            List[Dict[str, Any]]: List of deleted records.
        """
        column = column or self.primary_key
        query = self.supabase.table(self.table_name).delete().eq(column, value)
        return self._execute_query("delete", query)

    def filter(
        self, filters: List[Dict[str, Union[str, Any]]], select: str = "*"
    ) -> List[Dict[str, Any]]:
        """
        Filter records based on given conditions.

        Args:
            filters (List[Dict[str, Union[str, Any]]]): List of filter conditions.
                Each filter is a dict with keys: 'field', 'operator', and 'value'.
            select (str): Fields to select. Defaults to "*".

        Returns:
            List[Dict[str, Any]]: List of records matching the filter conditions.
        """
        query = self.supabase.table(self.table_name).select(select)
        for filter_condition in filters:
            field = filter_condition["field"]
            operator = FilterOperator(filter_condition["operator"])
            value = filter_condition["value"]
            query = getattr(query, operator.value)(field, value)
        return self._execute_query("filter", query)
