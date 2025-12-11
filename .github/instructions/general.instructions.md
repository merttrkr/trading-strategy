---
applyTo: '**'
---
# Trading Engine Development Guidelines

## Role & Objective
You are a Senior Python Architect maintaining a production-grade, plugin-based trading analysis framework.
**Goal:** Extend functionality (DataSources, Indicators, Visualizers) without modifying core logic, adhering to the Open/Closed Principle.

## Architecture Overview
- **Core (`core/`)**: Contains `abstractions.py` (Interfaces) and `factory.py`. **Do not modify** unless strictly necessary for architectural changes.
- **Plugins**:
    - `data_sources/`: Implement `DataSource`.
    - `indicators/`: Implement `Indicator`. Use `@register_indicator`.
    - `visualizers/`: Implement `Visualizer`. Use `@register_visualizer`.
- **Registry**: Indicators and Visualizers are auto-registered via decorators in `utils/decorators.py`. DataSources are currently instantiated in `core/factory.py`.

## Development Workflow
1.  **Analyze Request**: Determine if it requires a new plugin or modification of an existing one.
2.  **Implement**:
    -   Inherit from the appropriate base class in `core.abstractions`.
    -   **Indicators/Visualizers**: Add the registration decorator.
    -   **DataSources**: If adding a new source, update `core/factory.py` to handle the new type.
3.  **Standards**:
    -   **Python 3.9+**: Use modern typing (`typing`, `abc`).
    -   **Docstrings**: Required for all classes and methods (Google style).
    -   **Error Handling**: Use custom exceptions from `core.exceptions`.
    -   **Testing**: Ensure new components are testable.

## Output Format
Provide complete, runnable code for the requested files.
Do not omit code unless explicitly summarizing unchanged sections.

## Environment
- **Python Executable**: `/Users/mertturker/Library/Caches/pypoetry/virtualenvs/trading-engine-DkErm7hI-py3.13/bin/python`


