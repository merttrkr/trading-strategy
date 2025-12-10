from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any
import pandas as pd

@dataclass
class DataFetchConfig:
    """Configuration for data fetching.

    Args:
        ticker: The stock ticker symbol.
        interval: The data interval (e.g., "1d", "1h"). Defaults to "1d".
        start_date: The start date for data fetching (YYYY-MM-DD).
        end_date: The end date for data fetching (YYYY-MM-DD).
    """
    ticker: str
    interval: str = "1d"
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@dataclass
class AnalysisResult:
    """Container for analysis results.

    Args:
        data: The raw market data.
        indicators: A dictionary of calculated indicators.
        metadata: Additional metadata about the analysis.
        timestamp: The timestamp of the analysis.
    """
    data: pd.DataFrame
    indicators: Dict[str, pd.Series] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
