from typing import Dict, Type, Callable, TypeVar
from core.abstractions import Indicator, Visualizer, Strategy

# Type variables bound to our abstract base classes so registries return
# concrete subclasses of the correct type.
TIndicator = TypeVar('TIndicator', bound=Indicator)
TVisualizer = TypeVar('TVisualizer', bound=Visualizer)
TStrategy = TypeVar('TStrategy', bound=Strategy)

_INDICATOR_REGISTRY: Dict[str, Type[Indicator]] = {}
_VISUALIZER_REGISTRY: Dict[str, Type[Visualizer]] = {}
_STRATEGY_REGISTRY: Dict[str, Type[Strategy]] = {}


def register_indicator(name: str) -> Callable[[Type[TIndicator]], Type[TIndicator]]:
    """Decorator to register an indicator class.

    Args:
        name: The name to register the indicator under.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls: Type[TIndicator]) -> Type[TIndicator]:
        _INDICATOR_REGISTRY[name] = cls
        return cls
    return decorator

def register_visualizer(name: str) -> Callable[[Type[TVisualizer]], Type[TVisualizer]]:
    """Decorator to register a visualizer class.

    Args:
        name: The name to register the visualizer under.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls: Type[TVisualizer]) -> Type[TVisualizer]:
        _VISUALIZER_REGISTRY[name] = cls
        return cls
    return decorator

def register_strategy(name: str) -> Callable[[Type[TStrategy]], Type[TStrategy]]:
    """Decorator to register a strategy class.

    Args:
        name: The name to register the strategy under.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls: Type[TStrategy]) -> Type[TStrategy]:
        _STRATEGY_REGISTRY[name] = cls
        return cls
    return decorator

def get_indicator_class(name: str) -> Type[Indicator]:
    """Retrieves an indicator class by name.

    Args:
        name: The name of the indicator.

    Returns:
        Type: The indicator class.

    Raises:
        KeyError: If the indicator is not found.
    """
    if name not in _INDICATOR_REGISTRY:
        raise KeyError(f"Indicator '{name}' not found in registry.")
    return _INDICATOR_REGISTRY[name]

def get_visualizer_class(name: str) -> Type[Visualizer]:
    """Retrieves a visualizer class by name.

    Args:
        name: The name of the visualizer.

    Returns:
        Type: The visualizer class.

    Raises:
        KeyError: If the visualizer is not found.
    """
    if name not in _VISUALIZER_REGISTRY:
        raise KeyError(f"Visualizer '{name}' not found in registry.")
    return _VISUALIZER_REGISTRY[name]

def get_strategy_class(name: str) -> Type[Strategy]:
    """Retrieves a strategy class by name.

    Args:
        name: The name of the strategy.

    Returns:
        Type: The strategy class.

    Raises:
        KeyError: If the strategy is not found.
    """
    if name not in _STRATEGY_REGISTRY:
        raise KeyError(f"Strategy '{name}' not found in registry.")
    return _STRATEGY_REGISTRY[name]
