from typing import Dict, Any, List
from core.abstractions import DataSource, Indicator, Visualizer
from core.models import DataFetchConfig
from core.exceptions import FactoryError, ConfigurationError
from utils.decorators import get_indicator_class, get_visualizer_class
from data_sources.yfinance_source import YFinanceDataSource
from data_sources.csv_source import CSVDataSource

class ComponentFactory:
    """Factory for creating trading engine components."""

    def __init__(self, config: Dict[str, Any]):
        """Initializes the factory with configuration.

        Args:
            config: The configuration dictionary.
        """
        self.config = config
        self._validate_config()

    def _validate_config(self) -> None:
        """Validates the configuration structure.

        Raises:
            ConfigurationError: If required sections are missing.
        """
        required_sections = ['data_source', 'indicators', 'visualizer']
        for section in required_sections:
            if section not in self.config:
                raise ConfigurationError(f"Missing required configuration section: '{section}'")

    def create_fetch_config(self) -> DataFetchConfig:
        """Creates the data fetch configuration.

        Returns:
            DataFetchConfig: The data fetch configuration object.

        Raises:
            ConfigurationError: If configuration is invalid.
        """
        ds_config = self.config.get('data_source', {})
        if 'ticker' not in ds_config:
             raise ConfigurationError("Data source configuration missing 'ticker'.")
        
        return DataFetchConfig(
            ticker=ds_config['ticker'],
            interval=ds_config.get('interval', '1d'),
            start_date=ds_config.get('start_date'),
            end_date=ds_config.get('end_date')
        )

    def create_data_source(self) -> DataSource:
        """Creates the data source instance.

        Returns:
            DataSource: The data source instance.

        Raises:
            FactoryError: If the data source type is not supported or implementation is missing.
            ConfigurationError: If data source type is not specified.
        """
        ds_config = self.config.get('data_source', {})
        source_type = ds_config.get('type')
        
        if not source_type:
            raise ConfigurationError("Data source type not specified.")

        # In Phase 1, we don't have concrete implementations yet.
        # This will be expanded in Phase 2.
        if source_type == 'yfinance':
             return YFinanceDataSource()
        elif source_type == 'csv':
             return CSVDataSource()
        else:
            raise FactoryError(f"Unsupported data source type: '{source_type}'")

    def create_indicators(self) -> List[Indicator]:
        """Creates the list of indicator instances.

        Returns:
            List[Indicator]: A list of initialized indicator instances.

        Raises:
            FactoryError: If an indicator cannot be created.
        """
        indicators = []
        ind_configs = self.config.get('indicators', [])
        
        for ind_conf in ind_configs:
            name = ind_conf.get('name')
            if not name:
                continue 
            
            try:
                ind_cls = get_indicator_class(name)
                # Pass all other config parameters to the constructor
                params = {k: v for k, v in ind_conf.items() if k != 'name'}
                indicators.append(ind_cls(**params))
            except KeyError:
                raise FactoryError(f"Indicator '{name}' is not registered.")
            except Exception as e:
                raise FactoryError(f"Failed to create indicator '{name}': {str(e)}")
                
        return indicators

    def create_visualizer(self) -> Visualizer:
        """Creates the visualizer instance.

        Returns:
            Visualizer: The visualizer instance.

        Raises:
            FactoryError: If the visualizer cannot be created.
            ConfigurationError: If visualizer name is not specified.
        """
        vis_config = self.config.get('visualizer', {})
        name = vis_config.get('name')
        
        if not name:
            raise ConfigurationError("Visualizer name not specified.")
            
        try:
            vis_cls = get_visualizer_class(name)
            params = {k: v for k, v in vis_config.items() if k != 'name'}
            return vis_cls(**params)
        except KeyError:
            raise FactoryError(f"Visualizer '{name}' is not registered.")
        except Exception as e:
            raise FactoryError(f"Failed to create visualizer '{name}': {str(e)}")
