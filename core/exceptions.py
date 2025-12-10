class TradingEngineError(Exception):
    """Base exception for the trading engine."""
    pass

class DataFetchError(TradingEngineError):
    """Raised when data fetching fails."""
    pass

class IndicatorCalculationError(TradingEngineError):
    """Raised when indicator calculation fails."""
    pass

class VisualizationError(TradingEngineError):
    """Raised when visualization fails."""
    pass

class ConfigurationError(TradingEngineError):
    """Raised when configuration is invalid."""
    pass

class FactoryError(TradingEngineError):
    """Raised when component creation fails."""
    pass
