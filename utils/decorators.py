from typing import Dict, Type, Callable

_INDICATOR_REGISTRY: Dict[str, Type] = {}
_VISUALIZER_REGISTRY: Dict[str, Type] = {}

def register_indicator(name: str) -> Callable[[Type], Type]:
    """Decorator to register an indicator class.

    Args:
        name: The name to register the indicator under.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls: Type) -> Type:
        _INDICATOR_REGISTRY[name] = cls
        return cls
    return decorator

def register_visualizer(name: str) -> Callable[[Type], Type]:
    """Decorator to register a visualizer class.

    Args:
        name: The name to register the visualizer under.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls: Type) -> Type:
        _VISUALIZER_REGISTRY[name] = cls
        return cls
    return decorator

def get_indicator_class(name: str) -> Type:
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

def get_visualizer_class(name: str) -> Type:
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
