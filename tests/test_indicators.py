import pytest
import pandas as pd
import numpy as np
from indicators.moving_averages import SimpleMovingAverage, ExponentialMovingAverage
from indicators.oscillators import RelativeStrengthIndex
from core.exceptions import IndicatorCalculationError

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    })

def test_sma_calculation(sample_data):
    sma = SimpleMovingAverage(period=5)
    result = sma.calculate(sample_data)
    
    assert len(result) == len(sample_data)
    # First 4 should be NaN
    assert pd.isna(result.iloc[3])
    # 5th element (index 4) should be average of 10, 11, 12, 13, 14 = 12
    assert result.iloc[4] == 12.0
    assert sma.type == "overlay"

def test_sma_missing_column():
    sma = SimpleMovingAverage(period=5)
    df = pd.DataFrame({'Open': [10]})
    with pytest.raises(IndicatorCalculationError, match="'Close' column missing"):
        sma.calculate(df)

def test_ema_calculation(sample_data):
    ema = ExponentialMovingAverage(period=5)
    result = ema.calculate(sample_data)
    
    assert len(result) == len(sample_data)
    assert not pd.isna(result.iloc[0]) # EMA usually starts with first value or similar
    assert ema.type == "overlay"

def test_rsi_calculation():
    # Create a pattern of gains and losses
    # Up, Up, Down, Down
    prices = [10, 12, 14, 13, 12, 14, 16, 15, 14]
    df = pd.DataFrame({'Close': prices})
    
    rsi = RelativeStrengthIndex(period=2)
    result = rsi.calculate(df)
    
    assert len(result) == len(df)
    assert rsi.type == "oscillator"
    # RSI should be between 0 and 100
    assert result.dropna().between(0, 100).all()

def test_rsi_missing_column():
    rsi = RelativeStrengthIndex(period=14)
    df = pd.DataFrame({'Open': [10]})
    with pytest.raises(IndicatorCalculationError, match="'Close' column missing"):
        rsi.calculate(df)
