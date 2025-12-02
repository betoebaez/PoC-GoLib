"""
LibCoreHey - Python wrapper for HeyBanco Go library

This package provides Python bindings for HeyBanco's core functionality
implemented in Go, including APIs for Quick Replies and Typification.
"""

from .core import (
    get_quick_replies,
    get_typification,
    get_quick_replies_simple,
    get_typification_simple,
    get_quick_replies_ultra_simple,
    get_typification_ultra_simple,
    create_azure_config,
    add_numbers,
    multiply_numbers,
    get_fibonacci,
    is_prime,
    LibCoreHeyError
)

__version__ = "1.0.0"
__author__ = "HeyBanco Team"
__email__ = "dev@heybanco.com"

__all__ = [
    "get_quick_replies",
    "get_typification",
    "get_quick_replies_simple",
    "get_typification_simple",
    "get_quick_replies_ultra_simple",
    "get_typification_ultra_simple", 
    "create_azure_config",
    "add_numbers",
    "multiply_numbers",
    "get_fibonacci",
    "is_prime",
    "LibCoreHeyError"
]