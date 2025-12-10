import pandas as pd
from core.abstractions import Indicator
from core.exceptions import IndicatorCalculationError
from utils.decorators import register_indicator
from utils.logging import setup_logger
from typing import Literal

logger = setup_logger(__name__)

@register_indicator("SMA")
class SimpleMovingAverage(Indicator):
    """Simple Moving Average indicator."""

    def __init__(self, period: int = 20):
        self.period = period
        self._name = f"SMA_{period}"
        self._type: Literal["overlay", "oscillator"] = "overlay"
        logger.debug(f"Initialized {self.name}")

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> Literal["overlay", "oscillator"]:
        return self._type

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        try:
            if 'Close' not in df.columns:
                raise IndicatorCalculationError(f"{self.name}: 'Close' column missing")
            return df['Close'].rolling(window=self.period).mean()
        except Exception as e:
            raise IndicatorCalculationError(f"{self.name} calculation failed: {e}") from e

@register_indicator("EMA")
class ExponentialMovingAverage(Indicator):
    """Exponential Moving Average indicator."""

    def __init__(self, period: int = 20):
        self.period = period
        self._name = f"EMA_{period}"
        self._type: Literal["overlay", "oscillator"] = "overlay"
        logger.debug(f"Initialized {self.name}")

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> Literal["overlay", "oscillator"]:
        return self._type

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        try:
            if 'Close' not in df.columns:
                raise IndicatorCalculationError(f"{self.name}: 'Close' column missing")
            return df['Close'].ewm(span=self.period, adjust=False).mean()
        except Exception as e:
            raise IndicatorCalculationError(f"{self.name} calculation failed: {e}") from e
