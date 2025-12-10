import pytest
import os
import time
import shutil
import logging
from utils.cache import TTLCache, cached
from utils.decorators import register_indicator, register_visualizer, get_indicator_class, get_visualizer_class, _INDICATOR_REGISTRY, _VISUALIZER_REGISTRY
from utils.logging import setup_logger
from core.abstractions import Indicator, Visualizer

# --- Tests for utils/cache.py ---

@pytest.fixture
def cache_dir():
    dir_name = ".test_cache"
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    yield dir_name
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

def test_ttl_cache_set_get(cache_dir):
    cache = TTLCache(cache_dir=cache_dir, ttl_seconds=10)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"

def test_ttl_cache_expiry(cache_dir):
    cache = TTLCache(cache_dir=cache_dir, ttl_seconds=1)
    cache.set("key1", "value1")
    time.sleep(1.1)
    assert cache.get("key1") is None

def test_cached_decorator(cache_dir):
    call_count = 0

    @cached(cache_dir=cache_dir, ttl_seconds=10)
    def expensive_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive_func(2) == 4
    assert call_count == 1
    
    # Should be cached
    assert expensive_func(2) == 4
    assert call_count == 1
    
    # Different arg
    assert expensive_func(3) == 6
    assert call_count == 2

def test_cached_decorator_skip_cache(cache_dir):
    call_count = 0

    @cached(cache_dir=cache_dir, ttl_seconds=10)
    def expensive_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    expensive_func(2)
    assert call_count == 1
    
    # Skip cache
    expensive_func(2, _skip_cache=True)
    assert call_count == 2

# --- Tests for utils/decorators.py ---

def test_register_indicator():
    # Clear registry for test
    _INDICATOR_REGISTRY.clear()
    
    @register_indicator("TestInd")
    class TestIndicator(Indicator):
        pass
        
    assert "TestInd" in _INDICATOR_REGISTRY
    assert get_indicator_class("TestInd") == TestIndicator

def test_get_indicator_class_not_found():
    with pytest.raises(KeyError):
        get_indicator_class("NonExistent")

def test_register_visualizer():
    # Clear registry for test
    _VISUALIZER_REGISTRY.clear()
    
    @register_visualizer("TestVis")
    class TestVisualizer(Visualizer):
        pass
        
    assert "TestVis" in _VISUALIZER_REGISTRY
    assert get_visualizer_class("TestVis") == TestVisualizer

def test_get_visualizer_class_not_found():
    with pytest.raises(KeyError):
        get_visualizer_class("NonExistent")

# --- Tests for utils/logging.py ---

def test_setup_logger():
    logger = setup_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    # Check if console handler is added
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

def test_setup_logger_with_file(tmp_path):
    log_file = tmp_path / "test.log"
    logger = setup_logger("test_file_logger", log_file=str(log_file))
    
    # Verify root logger has file handler
    root_logger = logging.getLogger()
    assert any(isinstance(h, logging.FileHandler) and h.baseFilename == str(log_file) for h in root_logger.handlers)
