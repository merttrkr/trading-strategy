import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from data_sources.csv_source import CSVDataSource
from data_sources.yfinance_source import YFinanceDataSource
from core.models import DataFetchConfig
from core.exceptions import DataFetchError

# --- Tests for CSVDataSource ---

@pytest.fixture
def sample_csv_data():
    return pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02'],
        'Open': [100, 101],
        'High': [105, 106],
        'Low': [95, 96],
        'Close': [102, 103],
        'Volume': [1000, 1100]
    })

@patch('data_sources.csv_source.pd.read_csv')
@patch('data_sources.csv_source.os.path.exists')
def test_csv_fetch_success(mock_exists, mock_read_csv, sample_csv_data):
    mock_exists.return_value = True
    mock_read_csv.return_value = sample_csv_data
    
    source = CSVDataSource("dummy.csv")
    config = DataFetchConfig(ticker="AAPL")
    
    df = source.fetch_data(config)
    assert not df.empty
    assert len(df) == 2
    assert 'Close' in df.columns

@patch('data_sources.csv_source.os.path.exists')
def test_csv_file_not_found(mock_exists):
    mock_exists.return_value = False
    source = CSVDataSource("dummy.csv")
    config = DataFetchConfig(ticker="AAPL")
    
    with pytest.raises(DataFetchError, match="CSV file not found"):
        source.fetch_data(config)

@patch('data_sources.csv_source.pd.read_csv')
@patch('data_sources.csv_source.os.path.exists')
def test_csv_missing_columns(mock_exists, mock_read_csv):
    mock_exists.return_value = True
    mock_read_csv.return_value = pd.DataFrame({'Date': [], 'Open': []}) # Missing others
    
    source = CSVDataSource("dummy.csv")
    config = DataFetchConfig(ticker="AAPL")
    
    with pytest.raises(DataFetchError, match="Missing columns"):
        source.fetch_data(config)

# --- Tests for YFinanceDataSource ---

@patch('data_sources.yfinance_source.yf.download')
def test_yfinance_fetch_success(mock_download):
    mock_df = pd.DataFrame({
        'Open': [100], 'High': [105], 'Low': [95], 'Close': [102], 'Volume': [1000]
    }, index=pd.to_datetime(['2023-01-01']))
    mock_download.return_value = mock_df
    
    source = YFinanceDataSource()
    config = DataFetchConfig(ticker="AAPL")
    
    df = source.fetch_data(config)
    assert not df.empty
    assert 'Close' in df.columns

@patch('data_sources.yfinance_source.yf.download')
def test_yfinance_no_data(mock_download):
    mock_download.return_value = pd.DataFrame()
    
    source = YFinanceDataSource()
    config = DataFetchConfig(ticker="INVALID")
    
    with pytest.raises(DataFetchError, match="No data found"):
        source.fetch_data(config)

@patch('data_sources.yfinance_source.yf.download')
def test_yfinance_missing_columns(mock_download):
    mock_df = pd.DataFrame({'Open': [100]}) # Missing others
    mock_download.return_value = mock_df
    
    source = YFinanceDataSource()
    config = DataFetchConfig(ticker="AAPL")
    
    with pytest.raises(DataFetchError, match="Missing columns"):
        source.fetch_data(config)
