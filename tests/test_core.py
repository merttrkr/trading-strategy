import pytest
from datetime import datetime
import pandas as pd
from core.models import DataFetchConfig, AnalysisResult
from core.factory import ComponentFactory
from core.exceptions import ConfigurationError, FactoryError
from core.abstractions import DataSource, Indicator, Visualizer
from data_sources.yfinance_source import YFinanceDataSource
from data_sources.csv_source import CSVDataSource

# --- Tests for core/models.py ---

def test_data_fetch_config_defaults():
    config = DataFetchConfig(ticker="AAPL")
    assert config.ticker == "AAPL"
    assert config.interval == "1d"
    assert config.start_date is None
    assert config.end_date is None

def test_analysis_result_initialization():
    df = pd.DataFrame({'Close': [100, 101]})
    result = AnalysisResult(data=df)
    assert result.data.equals(df)
    assert result.indicators == {}
    assert isinstance(result.timestamp, datetime)

# --- Tests for core/factory.py ---

@pytest.fixture
def valid_config():
    return {
        'data_source': {'type': 'yfinance', 'ticker': 'AAPL'},
        'indicators': [{'name': 'SMA', 'period': 20}],
        'visualizer': {'type': 'matplotlib'}
    }

def test_factory_initialization_valid(valid_config):
    factory = ComponentFactory(valid_config)
    assert factory.config == valid_config

def test_factory_initialization_missing_section():
    config = {'data_source': {}}
    with pytest.raises(ConfigurationError, match="Missing required configuration section"):
        ComponentFactory(config)

def test_create_fetch_config(valid_config):
    factory = ComponentFactory(valid_config)
    fetch_config = factory.create_fetch_config()
    assert isinstance(fetch_config, DataFetchConfig)
    assert fetch_config.ticker == "AAPL"

def test_create_fetch_config_missing_ticker(valid_config):
    valid_config['data_source'].pop('ticker')
    factory = ComponentFactory(valid_config)
    with pytest.raises(ConfigurationError, match="Data source configuration missing 'ticker'"):
        factory.create_fetch_config()

def test_create_data_source_yfinance(valid_config):
    factory = ComponentFactory(valid_config)
    ds = factory.create_data_source()
    assert isinstance(ds, YFinanceDataSource)

def test_create_data_source_csv(valid_config):
    valid_config['data_source']['type'] = 'csv'
    factory = ComponentFactory(valid_config)
    ds = factory.create_data_source()
    assert isinstance(ds, CSVDataSource)

def test_create_data_source_unsupported(valid_config):
    valid_config['data_source']['type'] = 'unknown'
    factory = ComponentFactory(valid_config)
    with pytest.raises(FactoryError, match="Unsupported data source type"):
        factory.create_data_source()

def test_create_data_source_missing_type(valid_config):
    valid_config['data_source'].pop('type')
    factory = ComponentFactory(valid_config)
    with pytest.raises(ConfigurationError, match="Data source type not specified"):
        factory.create_data_source()

def test_create_indicators(valid_config):
    # Ensure SMA is registered (it might be imported by factory or we need to import it)
    from indicators.moving_averages import SimpleMovingAverage
    
    factory = ComponentFactory(valid_config)
    indicators = factory.create_indicators()
    assert len(indicators) == 1
    assert isinstance(indicators[0], SimpleMovingAverage)
    assert indicators[0].period == 20

def test_create_indicators_unregistered(valid_config):
    valid_config['indicators'] = [{'name': 'UnknownIndicator'}]
    factory = ComponentFactory(valid_config)
    with pytest.raises(FactoryError, match="Indicator 'UnknownIndicator' is not registered"):
        factory.create_indicators()
