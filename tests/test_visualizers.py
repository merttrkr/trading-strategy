import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from visualizers.mpl_visualizer import MatplotlibVisualizer
from core.exceptions import VisualizationError

@pytest.fixture
def sample_data():
    dates = pd.date_range(start='2023-01-01', periods=5)
    df = pd.DataFrame({
        'Open': [100, 101, 102, 103, 104],
        'High': [105, 106, 107, 108, 109],
        'Low': [95, 96, 97, 98, 99],
        'Close': [102, 103, 104, 105, 106],
        'Volume': [1000, 1100, 1200, 1300, 1400]
    }, index=dates)
    return df

@pytest.fixture
def sample_indicators(sample_data):
    return {
        'SMA_20': pd.Series([100]*5, index=sample_data.index),
        'RSI_14': pd.Series([50]*5, index=sample_data.index)
    }

@patch('visualizers.mpl_visualizer.mpf.plot')
def test_render_success(mock_plot, sample_data, sample_indicators, tmp_path):
    visualizer = MatplotlibVisualizer()
    output_path = str(tmp_path / "chart.png")
    
    visualizer.render(sample_data, sample_indicators, output_path)
    
    assert mock_plot.called
    args, kwargs = mock_plot.call_args
    assert args[0].equals(sample_data)
    assert kwargs['savefig'] == output_path
    assert len(kwargs['addplot']) == 2 # SMA and RSI

@patch('visualizers.mpl_visualizer.mpf.plot')
def test_render_failure(mock_plot, sample_data, sample_indicators):
    mock_plot.side_effect = Exception("Plotting error")
    visualizer = MatplotlibVisualizer()
    
    with pytest.raises(VisualizationError, match="Visualization failed"):
        visualizer.render(sample_data, sample_indicators, "dummy.png")
