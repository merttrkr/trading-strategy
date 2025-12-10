import mplfinance as mpf
import pandas as pd
from typing import Dict
from core.abstractions import Visualizer
from core.exceptions import VisualizationError
from utils.decorators import register_visualizer
from utils.logging import setup_logger

logger = setup_logger(__name__)

@register_visualizer("matplotlib")
class MatplotlibVisualizer(Visualizer):
    """Visualizer using mplfinance."""

    def __init__(self, **kwargs):
        """Initializes the visualizer.

        Args:
            **kwargs: Configuration parameters.
        """
        self.config = kwargs

    def render(self, df: pd.DataFrame, indicators: Dict[str, pd.Series], output_path: str) -> None:
        """Renders the analysis results to a file using mplfinance.

        Args:
            df: The market data.
            indicators: A dictionary of calculated indicators.
            output_path: The path to save the visualization.

        Raises:
            VisualizationError: If visualization fails.
        """
        try:
            logger.info(f"Rendering chart to {output_path}...")
            
            # Prepare addplots
            apds = []
            
            # Overlay indicators (Panel 0)
            for name, series in indicators.items():
                # Heuristic: if name starts with SMA or EMA, it's overlay
                # But we don't have the indicator object here, just the series.
                # The prompt says: "Add overlay indicators (SMA, EMA) to price panel (panel=0)"
                # "Add oscillator indicators (RSI) to separate panel (panel=1)"
                
                if name.startswith("SMA") or name.startswith("EMA"):
                    apds.append(mpf.make_addplot(series, panel=0, width=1.0))
                elif name.startswith("RSI"):
                    apds.append(mpf.make_addplot(series, panel=1, width=1.0, ylabel='RSI'))
            
            # Create the plot
            # We need to ensure the directory exists
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            mpf.plot(
                df,
                type='candle',
                style='yahoo',
                volume=True,
                addplot=apds,
                savefig=output_path,
                panel_ratios=(6, 2) if any(n.startswith("RSI") for n in indicators) else (1,),
                title=f"Analysis Result"
            )
            
            logger.info(f"Chart saved to {output_path}")

        except Exception as e:
            logger.error(f"Visualization failed: {e}")
            raise VisualizationError(f"Visualization failed: {e}") from e
