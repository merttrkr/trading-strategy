from abc import ABC, abstractmethod
from typing import Dict, Literal
import pandas as pd
from core.models import DataFetchConfig

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

class Visualizer(ABC):
    """Abstract base class for data visualization."""
    
    @abstractmethod
    def render(self, df: pd.DataFrame, indicators: Dict[str, pd.Series], output_path: str) -> None:
        """Renders the analysis results to a file.

        Args:
            df: The market data.
            indicators: A dictionary of calculated indicators.
            output_path: The path to save the visualization.

        Raises:
            VisualizationError: If visualization fails.
        """
        pass
