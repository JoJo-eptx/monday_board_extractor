"""
MondayColumnExtractor: Extracts column data from Monday.com boards using the Monday.com API.
"""

import pandas as pd
import requests
import logging

from typing import List
from .monday_base_class import BaseExtractor, BoardData

logging.basicConfig(level=logging.INFO)


class MondayColumnExtractor(BaseExtractor):
    """
    Extractor for retrieving column data from Monday.com boards.

    Inherits from BaseExtractor and implements methods to build queries,
    fetch data from the Monday.com API, and convert the results to pandas DataFrames.
    """

    def __init__(self, api_key: str, board_ids: list):
        """
        Initialize the MondayColumnExtractor.

        Args:
            api_key (str): Monday.com API key.
            board_ids (list): List of board IDs to extract data from.
        """
        super().__init__(api_key, board_ids)
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    def _build_query_0(self) -> str:
        """
        Build the GraphQL query for retrieving board column data.

        Returns:
            str: The GraphQL query string.
        """
        board_ids_str = ', '.join(map(str, self.board_ids))
        return f'''
        query {{
          boards(ids: [{board_ids_str}]) {{
            name
            items_page {{
                items {{
                    id
                    column_values {{
                        id
                        text
                    }}
                }}
            }}
          }}
        }}
        '''
    
    def _build_query_1(self) -> str:
        board_ids_str = ', '.join(map(str, self.board_ids))
        return f'''
            query {{
                boards(ids: [{board_ids_str}]) {{
                    name
                    columns {{
                        id
                        title
                    }}
                    items_page {{
                        items {{
                            id
                            column_values {{
                                id
                                text
                            }}
                        }}
                    }}
                }}
            }}
    '''

    def _build_query(self) -> str:
        board_ids_str = ', '.join(map(str, self.board_ids))
        return f'''
            query {{
                boards(ids: [{board_ids_str}]) {{
                    name
                    columns {{
                        id
                        title
                    }}
                    items_page (limit: 500) {{
                        items {{
                            id
                            name  # This is the "Item" column
                            column_values {{
                                id
                                text
                            }}
                        }}
                    }}
                }}
            }}
        '''

    def _fetch_data(self):
        """
        Fetch data from the Monday.com API using the built query.

        Returns:
            dict: The JSON response from the API.
        Raises:
            requests.RequestException: If the request fails.
            Exception: For any other unexpected errors.
        """
        try:
            query = self._build_query()
            response = requests.post(self.url, json={'query': query}, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

    @staticmethod
    def _extract_to_dataframe(items):
        rows = []
        for item in items:
            column_values = item.get('column_values', [])
            row_dict = {col['id']: col.get('text') for col in column_values}
            row_dict['Item'] = item.get('name')  # Add "Item" column explicitly
            rows.append(row_dict)
        return pd.DataFrame(rows)

    @staticmethod
    def _extract_to_dataframe_0(items):
        """
        Convert a list of item dictionaries to a pandas DataFrame.

        Args:
            items (list): List of item dictionaries from the API response.
        Returns:
            pd.DataFrame: DataFrame containing the column data for each item.
        """
        rows = []
        for item in items:
            column_values = item.get('column_values', [])
            row_dict = {col['id']: col.get('text') for col in column_values}
            rows.append(row_dict)
        return pd.DataFrame(rows)

    def extract_0(self) -> List[BoardData]:
        """
        Extract and process board data from the Monday.com API.

        Returns:
            List[BoardData]: List of BoardData objects, each containing the board name and its data as a DataFrame.
        """
        data = self._fetch_data()
        boards = data['data']['boards']
        result = []

        for board in boards:
            name = board['name']
            items = board['items_page']['items']
            df = self._extract_to_dataframe(items)
            result.append(BoardData(name=name, data=df))

        return result
    
    def extract(self) -> List[BoardData]:
        data = self._fetch_data()
        boards = data['data']['boards']
        result = []

        for board in boards:
            name = board['name']
            items = board['items_page']['items']
            df = self._extract_to_dataframe(items)

            # Get column ID → title mapping
            column_map = {col['id']: col['title'] for col in board.get('columns', [])}

            # Rename columns to user-friendly labels
            df.rename(columns=column_map, inplace=True)

            result.append(BoardData(name=name, data=df))

        return result
