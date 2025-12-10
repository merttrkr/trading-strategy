from typing import List
from core.abstractions import DataSource, Indicator, Visualizer
from core.models import DataFetchConfig, AnalysisResult
from core.exceptions import TradingEngineError, DataFetchError, IndicatorCalculationError, VisualizationError
from utils.logging import setup_logger

class TradingEngine:
    """Orchestrates the trading analysis pipeline."""

    def __init__(self, data_source: DataSource, indicators: List[Indicator], visualizer: Visualizer):
        """Initializes the trading engine with dependencies.

        Args:
            data_source: The data source component.
            indicators: A list of indicator components.
            visualizer: The visualizer component.
        """
        self.data_source = data_source
        self.indicators = indicators
        self.visualizer = visualizer
        self.logger = setup_logger(__name__)

    def run(self, config: DataFetchConfig, output_path: str) -> AnalysisResult:
        """Execute the complete analysis pipeline.
        
        Args:
            config: Data fetch configuration
            output_path: Path to save visualization
            
        Returns:
            AnalysisResult containing all data and metadata
            
        Raises:
            DataFetchError: If data fetching fails
            IndicatorCalculationError: If any indicator calculation fails
            VisualizationError: If rendering fails
        """
        self.logger.info(f"Starting analysis for {config.ticker}")
        
        try:
            # 1. Fetch Data
            self.logger.info("Fetching market data...")
            df = self.data_source.fetch_data(config)
            self.logger.info(f"Fetched {len(df)} rows of data.")

            # 2. Calculate Indicators
            self.logger.info("Calculating indicators...")
            indicator_results = {}
            for indicator in self.indicators:
                self.logger.info(f"Calculating {indicator.name}...")
                try:
                    series = indicator.calculate(df)
                    indicator_results[indicator.name] = series
                except Exception as e:
                    self.logger.error(f"Error calculating {indicator.name}: {e}")
                    raise IndicatorCalculationError(f"Failed to calculate {indicator.name}: {e}") from e

            # 3. Render Visualization
            self.logger.info(f"Rendering visualization to {output_path}...")
            try:
                self.visualizer.render(df, indicator_results, output_path)
            except Exception as e:
                self.logger.error(f"Error rendering visualization: {e}")
                raise VisualizationError(f"Failed to render visualization: {e}") from e

            self.logger.info("Analysis completed successfully.")
            
            return AnalysisResult(
                data=df,
                indicators=indicator_results,
                metadata={"ticker": config.ticker, "interval": config.interval}
            )

        except TradingEngineError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in trading engine: {e}")
            raise TradingEngineError(f"An unexpected error occurred: {e}") from e
