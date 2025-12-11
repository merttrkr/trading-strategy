import mplfinance as mpf
import pandas as pd
from typing import Dict, List
from core.abstractions import Visualizer
from core.models import Signal, SignalType
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

    def render(self, df: pd.DataFrame, indicators: Dict[str, pd.Series], signals: List[Signal], output_path: str) -> None:
        """Renders the analysis results to a file using mplfinance.

        Args:
            df: The market data.
            indicators: A dictionary of calculated indicators.
            signals: A list of trading signals.
            output_path: The path to save the visualization.

        Raises:
            VisualizationError: If visualization fails.
        """
        try:
            logger.info(f"Rendering chart to {output_path}...")
            
            # Prepare addplots
            apds = []
            has_rsi = any(n.startswith("RSI") for n in indicators)
            
            # Overlay indicators (Panel 0)
            for name, series in indicators.items():
                # Heuristic: if name starts with SMA or EMA, it's overlay
                # But we don't have the indicator object here, just the series.
                # The prompt says: "Add overlay indicators (SMA, EMA) to price panel (panel=0)"
                # "Add oscillator indicators (RSI) to separate panel (panel=1)"
                
                if name.startswith("SMA") or name.startswith("EMA"):
                    logger.info(f"Adding overlay indicator: {name}")
                    apds.append(mpf.make_addplot(series, panel=0, width=1.5))
                elif name.startswith("RSI"):
                    logger.info(f"Adding oscillator indicator: {name}")
                    # Move RSI to panel 2 to avoid volume (panel 1)
                    apds.append(mpf.make_addplot(series, panel=2, width=1.0, ylabel='RSI'))
            
            logger.info(f"Total addplots: {len(apds)}")
            
            # Add signals
            if signals:
                buy_signals = [float('nan')] * len(df)
                sell_signals = [float('nan')] * len(df)
                
                for signal in signals:
                    if signal.timestamp in df.index:
                        # Use get_loc to find integer location, but we can just use the timestamp if index is datetime
                        # However, to populate the list, we need integer index.
                        try:
                            idx = df.index.get_loc(signal.timestamp)
                            # get_loc might return slice or array if duplicates, assuming unique index
                            if isinstance(idx, int):
                                if signal.type == SignalType.BUY:
                                    buy_signals[idx] = signal.price * 0.99 # Place marker below price
                                elif signal.type == SignalType.SELL:
                                    sell_signals[idx] = signal.price * 1.01 # Place marker above price
                        except KeyError:
                            continue

                # Check if we have any signals to plot to avoid empty plot warnings/errors if lists are all nan
                if not all(pd.isna(x) for x in buy_signals):
                    apds.append(mpf.make_addplot(buy_signals, type='scatter', markersize=100, marker='^', color='g', panel=0))
                if not all(pd.isna(x) for x in sell_signals):
                    apds.append(mpf.make_addplot(sell_signals, type='scatter', markersize=100, marker='v', color='r', panel=0))

            # Create the plot
            # We need to ensure the directory exists
            import os
            dirname = os.path.dirname(output_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            # Configure save options
            dpi = self.config.get('dpi', 300)
            savefig_args = dict(fname=output_path, dpi=dpi, bbox_inches='tight')

            # Determine panel ratios
            # If RSI is present, we have 3 panels: Price(0), Volume(1), RSI(2)
            # If no RSI, we have 2 panels: Price(0), Volume(1)
            panel_ratios = (6, 2, 2) if has_rsi else (6, 2)

            mpf.plot(
                df,
                type='candle',
                style='yahoo',
                volume=True,
                addplot=apds,
                savefig=savefig_args,
                panel_ratios=panel_ratios,
                title=f"Analysis Result"
            )
            
            logger.info(f"Chart saved to {output_path}")

        except Exception as e:
            logger.error(f"Visualization failed: {e}")
            raise VisualizationError(f"Visualization failed: {e}") from e
