from typing import Dict, List
import pandas as pd
from core.abstractions import Strategy
from core.models import Signal, SignalType
from utils.decorators import register_strategy

@register_strategy("sma_crossover")
class SMACrossoverStrategy(Strategy):
    """Simple Moving Average Crossover Strategy."""

    def __init__(self, fast_ma_name: str = "SMA_10", slow_ma_name: str = "SMA_50"):
        self.fast_ma_name = fast_ma_name
        self.slow_ma_name = slow_ma_name

    @property
    def name(self) -> str:
        return "SMA Crossover"

    def generate_signals(self, df: pd.DataFrame, indicators: Dict[str, pd.Series]) -> List[Signal]:
        signals = []
        
        if self.fast_ma_name not in indicators or self.slow_ma_name not in indicators:
            return signals

        fast_ma = indicators[self.fast_ma_name]
        slow_ma = indicators[self.slow_ma_name]
        
        # Iterate through the data to find crossovers
        for i in range(1, len(df)):
            timestamp = df.index[i]
            # Handle different column naming conventions if necessary, but assuming 'Close' is standard
            price = df['Close'].iloc[i] 
            
            curr_fast = fast_ma.iloc[i]
            curr_slow = slow_ma.iloc[i]
            prev_fast = fast_ma.iloc[i-1]
            prev_slow = slow_ma.iloc[i-1]
            
            if pd.isna(curr_fast) or pd.isna(curr_slow) or pd.isna(prev_fast) or pd.isna(prev_slow):
                continue

            # Buy Signal: Fast crosses above Slow
            if prev_fast <= prev_slow and curr_fast > curr_slow:
                signals.append(Signal(
                    timestamp=timestamp, 
                    type=SignalType.BUY, 
                    price=price, 
                    description=f"Golden Cross: {self.fast_ma_name} crossed above {self.slow_ma_name}"
                ))
            # Sell Signal: Fast crosses below Slow
            elif prev_fast >= prev_slow and curr_fast < curr_slow:
                signals.append(Signal(
                    timestamp=timestamp, 
                    type=SignalType.SELL, 
                    price=price, 
                    description=f"Death Cross: {self.fast_ma_name} crossed below {self.slow_ma_name}"
                ))
                
        return signals
