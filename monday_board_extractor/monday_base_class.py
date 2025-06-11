"""
Base classes and data structures for Monday.com board extraction.
"""

from abc import ABC, abstractmethod
import pandas as pd
from dataclasses import dataclass

@dataclass
class BoardData:
    """
    Data class to store the name and data (as a DataFrame) for a Monday.com board.
    """
    name: str
    data: pd.DataFrame

class BaseExtractor(ABC):
    """
    Abstract base class for Monday.com board extractors.

    Args:
        api_key (str): Monday.com API key.
        board_ids (list): List of board IDs to extract data from.
    """
    def __init__(self, api_key: str, board_ids: list):
        """
        Initialize the extractor with API key and board IDs.
        """
        self.api_key = api_key
        self.board_ids = board_ids

    @abstractmethod
    def _build_query(self) -> str:
        """
        Build the GraphQL query for Monday.com API.
        Returns:
            str: The GraphQL query string.
        """
        pass

    @abstractmethod
    def _fetch_data(self):
        """
        Fetch data from the Monday.com API.
        Returns:
            Any: The raw data fetched from the API.
        """
        pass

    @abstractmethod
    def extract(self) -> dict:
        """
        Extract and process data from the Monday.com API.
        Returns:
            dict: Processed data, typically as a dictionary of BoardData objects.
        """
        pass