import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from core.abstractions import DataSource
from core.models import DataFetchConfig
from core.exceptions import DataFetchError
from utils.logging import setup_logger

logger = setup_logger(__name__)

class YFinanceDataSource(DataSource):
    """Data source implementation using yfinance."""

    def fetch_data(self, config: DataFetchConfig) -> pd.DataFrame:
        """Fetches market data using yfinance.

        Args:
            config: The data fetch configuration.

        Returns:
            pd.DataFrame: The fetched market data with columns ['Open', 'High', 'Low', 'Close', 'Volume'].

        Raises:
            DataFetchError: If data fetching fails.
        """
        try:
            logger.info(f"Fetching data for {config.ticker}...")
            
            start_date = config.start_date
            end_date = config.end_date
            
            # Default to last 90 days if not specified
            if not start_date:
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')

            df = yf.download(
                config.ticker,
                start=start_date,
                end=end_date,
                interval=config.interval,
                progress=False
            )

            if df.empty:
                raise DataFetchError(f"No data found for {config.ticker}")

            # Ensure columns exist and are properly named
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Handle MultiIndex columns if they exist (yfinance update)
            if isinstance(df.columns, pd.MultiIndex):
                 df.columns = df.columns.get_level_values(0)
            
            # Check if columns are present
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                 raise DataFetchError(f"Missing columns in fetched data: {missing_cols}")

            df = df[required_cols]
            
            # Ensure index is timezone-naive DatetimeIndex
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            
            logger.info(f"Successfully fetched {len(df)} rows for {config.ticker}")
            return df

        except Exception as e:
            logger.error(f"Failed to fetch data for {config.ticker}: {e}")
            raise DataFetchError(f"Failed to fetch data for {config.ticker}: {e}") from e
