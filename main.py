import argparse
import sys
import yaml
from typing import Dict, Any

# Import core components
from core.factory import ComponentFactory
from core.exceptions import TradingEngineError
from engine import TradingEngine
from utils.logging import setup_logger

# Import plugins to ensure registration
import data_sources
import indicators
import visualizers

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Trading Analysis Engine')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--ticker', help='Override ticker from config')
    parser.add_argument('--interval', help='Override interval from config')
    parser.add_argument('--output', help='Override output path from config')
    
    args = parser.parse_args()
    
    # Load config
    config_data = load_config(args.config)
    
    # Apply CLI overrides
    if args.ticker:
        if 'data_source' not in config_data:
            config_data['data_source'] = {}
        config_data['data_source']['ticker'] = args.ticker
        
    if args.interval:
        if 'data_source' not in config_data:
            config_data['data_source'] = {}
        config_data['data_source']['interval'] = args.interval
        
    if args.output:
        if 'visualizer' not in config_data:
            config_data['visualizer'] = {}
        config_data['visualizer']['output_path'] = args.output

    # Setup logging
    log_config = config_data.get('logging', {})
    log_file = log_config.get('file')
    logger = setup_logger('main', log_file)
    
    logger.info("Initializing Trading Engine...")
    
    try:
        # Create factory
        factory = ComponentFactory(config_data)
        
        # Create components
        data_source = factory.create_data_source()
        indicators_list = factory.create_indicators()
        visualizer = factory.create_visualizer()
        
        # Create engine
        engine = TradingEngine(data_source, indicators_list, visualizer)
        
        # Create fetch config
        fetch_config = factory.create_fetch_config()
        
        # Get output path
        output_path = config_data.get('visualizer', {}).get('output_path', 'results/outputs/chart.png')
        
        # Run engine
        engine.run(fetch_config, output_path)
        
    except TradingEngineError as e:
        logger.error(f"Trading Engine Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
