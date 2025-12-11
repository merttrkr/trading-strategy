from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any, List
from enum import Enum, auto
import pandas as pd

class SignalType(Enum):
    """Enumeration of signal types."""
    BUY = auto()
    SELL = auto()
    HOLD = auto()

@dataclass
class Signal:
    """Represents a trading signal.

    Args:
        timestamp: The time of the signal.
        type: The type of signal (BUY, SELL, HOLD).
        price: The price at which the signal was generated.
        description: Optional description or reason for the signal.
    """
    timestamp: datetime
    type: SignalType
    price: float
    description: str = ""

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
    signals: List[Signal] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
