import pandas as pd
import os
from core.abstractions import DataSource
from core.models import DataFetchConfig
from core.exceptions import DataFetchError
from utils.logging import setup_logger

logger = setup_logger(__name__)

class CSVDataSource(DataSource):
    """Data source implementation using CSV files."""

    def __init__(self, csv_path: str = "data/ohlcv.csv"):
        """Initializes the CSV data source.

        Args:
            csv_path: Path to the CSV file.
        """
        self.csv_path = csv_path

    def fetch_data(self, config: DataFetchConfig) -> pd.DataFrame:
        """Fetches market data from a CSV file.

        Args:
            config: The data fetch configuration.

        Returns:
            pd.DataFrame: The fetched market data.

        Raises:
            DataFetchError: If file not found or columns missing.
        """
        try:
            logger.info(f"Loading data from {self.csv_path}...")
            
            if not os.path.exists(self.csv_path):
                raise DataFetchError(f"CSV file not found: {self.csv_path}")

            df = pd.read_csv(self.csv_path)
            
            # Normalize column names to title case to match expected format
            df.columns = [c.title() for c in df.columns]
            
            required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                raise DataFetchError(f"Missing columns in CSV: {missing_cols}")

            # Set Date as index
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
            # Filter by date if provided in config
            if config.start_date:
                df = df[df.index >= pd.to_datetime(config.start_date)]
            if config.end_date:
                df = df[df.index <= pd.to_datetime(config.end_date)]

            logger.info(f"Successfully loaded {len(df)} rows from CSV")
            return df

        except Exception as e:
            logger.error(f"Failed to load data from CSV: {e}")
            raise DataFetchError(f"Failed to load data from CSV: {e}") from e
