import pytest
import pandas as pd
from unittest.mock import MagicMock
from engine import TradingEngine
from core.models import DataFetchConfig, AnalysisResult
from core.exceptions import DataFetchError, IndicatorCalculationError, VisualizationError

@pytest.fixture
def mock_data_source():
    ds = MagicMock()
    ds.fetch_data.return_value = pd.DataFrame({'Close': [100, 101, 102]})
    return ds

@pytest.fixture
def mock_indicator():
    ind = MagicMock()
    ind.name = "TestInd"
    ind.calculate.return_value = pd.Series([1, 2, 3])
    return ind

@pytest.fixture
def mock_visualizer():
    return MagicMock()

@pytest.fixture
def engine(mock_data_source, mock_indicator, mock_visualizer):
    return TradingEngine(mock_data_source, [mock_indicator], mock_visualizer)

def test_run_success(engine, mock_data_source, mock_indicator, mock_visualizer):
    config = DataFetchConfig(ticker="AAPL")
    result = engine.run(config, "output.png")
    
    assert isinstance(result, AnalysisResult)
    mock_data_source.fetch_data.assert_called_once_with(config)
    mock_indicator.calculate.assert_called_once()
    mock_visualizer.render.assert_called_once()

def test_run_data_fetch_error(engine, mock_data_source):
    mock_data_source.fetch_data.side_effect = DataFetchError("Fetch failed")
    config = DataFetchConfig(ticker="AAPL")
    
    with pytest.raises(DataFetchError):
        engine.run(config, "output.png")

def test_run_indicator_error(engine, mock_indicator):
    mock_indicator.calculate.side_effect = Exception("Calc failed")
    config = DataFetchConfig(ticker="AAPL")
    
    with pytest.raises(IndicatorCalculationError):
        engine.run(config, "output.png")

def test_run_visualization_error(engine, mock_visualizer):
    mock_visualizer.render.side_effect = Exception("Render failed")
    config = DataFetchConfig(ticker="AAPL")
    
    with pytest.raises(VisualizationError):
        engine.run(config, "output.png")
