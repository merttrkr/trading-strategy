import pandas as pd
from core.abstractions import Indicator
from core.exceptions import IndicatorCalculationError
from utils.decorators import register_indicator
from utils.logging import setup_logger
from typing import Literal

logger = setup_logger(__name__)

@register_indicator("RSI")
class RelativeStrengthIndex(Indicator):
    """Relative Strength Index indicator."""

    def __init__(self, period: int = 14):
        self.period = period
        self._name = f"RSI_{period}"
        self._type: Literal["overlay", "oscillator"] = "oscillator"
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
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()

            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            raise IndicatorCalculationError(f"{self.name} calculation failed: {e}") from e
