from abc import ABC, abstractmethod
from typing import Dict, Literal, List
import pandas as pd
from core.models import DataFetchConfig, Signal

class DataSource(ABC):
    """Abstract base class for data sources."""
    
    @abstractmethod
    def fetch_data(self, config: DataFetchConfig) -> pd.DataFrame:
        """Fetches market data based on configuration.

        Args:
            config: The data fetch configuration.

        Returns:
            pd.DataFrame: The fetched market data.

        Raises:
            DataFetchError: If data fetching fails.
        """
        pass

class Indicator(ABC):
    """Abstract base class for technical indicators."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the display name of the indicator."""
        pass

    @property
    @abstractmethod
    def type(self) -> Literal["overlay", "oscillator"]:
        """Returns the type of the indicator."""
        pass

    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        """Calculates the indicator values.

        Args:
            df: The market data.

        Returns:
            pd.Series: The calculated indicator values.

        Raises:
            IndicatorCalculationError: If calculation fails.
        """
        pass

class Strategy(ABC):
    """Abstract base class for trading strategies."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the display name of the strategy."""
        pass

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame, indicators: Dict[str, pd.Series]) -> List[Signal]:
        """Generates trading signals based on data and indicators.

        Args:
            df: The market data.
            indicators: A dictionary of calculated indicators.

        Returns:
            List[Signal]: A list of generated trading signals.
        """
        pass

class Visualizer(ABC):
    """Abstract base class for data visualization."""
    
    @abstractmethod
    def render(self, df: pd.DataFrame, indicators: Dict[str, pd.Series], signals: List[Signal], output_path: str) -> None:
        """Renders the analysis results to a file.

        Args:
            df: The market data.
            indicators: A dictionary of calculated indicators.
            signals: A list of trading signals.
            output_path: The path to save the visualization.

        Raises:
            VisualizationError: If visualization fails.
        """
        pass
