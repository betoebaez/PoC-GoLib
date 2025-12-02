"""
Core functionality for LibCoreHey package.

This module provides the main interface to the HeyBanco Go library
through Python bindings using ctypes.
"""

import ctypes
import os
import sys
import platform
from pathlib import Path
from typing import Optional


class LibCoreHeyError(Exception):
    """Base exception for LibCoreHey operations."""
    pass


class _LibraryLoader:
    """Handles loading the Go shared library with cross-platform support."""
    
    def __init__(self):
        self._lib = None
        self._loaded = False
    
    def _get_library_path(self) -> Path:
        """Get the path to the shared library based on platform."""
        package_dir = Path(__file__).parent
        
        system = platform.system().lower()
        if system == "darwin":  # macOS
            lib_name = "libcorehey.dylib"
        elif system == "linux":
            lib_name = "libcorehey.so"
        elif system == "windows":
            lib_name = "libcorehey.dll"
        else:
            raise LibCoreHeyError(f"Unsupported platform: {system}")
            
        return package_dir / lib_name
    
    def _setup_library_path(self):
        """Setup library path for dynamic loading."""
        package_dir = Path(__file__).parent
        
        if platform.system() == "Darwin":  # macOS
            # Set DYLD_LIBRARY_PATH for macOS
            current_path = os.environ.get('DYLD_LIBRARY_PATH', '')
            if str(package_dir) not in current_path:
                os.environ['DYLD_LIBRARY_PATH'] = f"{package_dir}:{current_path}".rstrip(':')
        elif platform.system() == "Linux":
            # Set LD_LIBRARY_PATH for Linux
            current_path = os.environ.get('LD_LIBRARY_PATH', '')
            if str(package_dir) not in current_path:
                os.environ['LD_LIBRARY_PATH'] = f"{package_dir}:{current_path}".rstrip(':')
    
    def load_library(self):
        """Load the Go shared library."""
        if self._loaded:
            return self._lib
        
        self._setup_library_path()
        lib_path = self._get_library_path()
        
        if not lib_path.exists():
            raise LibCoreHeyError(
                f"Shared library not found at {lib_path}. "
                f"Please ensure the library is properly built and installed."
            )
        
        try:
            self._lib = ctypes.CDLL(str(lib_path))
            self._configure_functions()
            self._loaded = True
            return self._lib
        except OSError as e:
            raise LibCoreHeyError(f"Failed to load library {lib_path}: {e}")
    
    def _configure_functions(self):
        """Configure function signatures for the Go library."""
        # GetQuickReplies function
        self._lib.GetQuickReplies.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self._lib.GetQuickReplies.restype = ctypes.c_char_p
        
        # GetTypification function  
        self._lib.GetTypification.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self._lib.GetTypification.restype = ctypes.c_char_p
        
        # FreeCString function
        self._lib.FreeCString.argtypes = [ctypes.c_char_p]
        self._lib.FreeCString.restype = None
        
        # Math functions (if they exist in the library)
        if hasattr(self._lib, 'Add'):
            self._lib.Add.argtypes = [ctypes.c_int, ctypes.c_int]
            self._lib.Add.restype = ctypes.c_int
        
        if hasattr(self._lib, 'Multiply'):
            self._lib.Multiply.argtypes = [ctypes.c_int, ctypes.c_int]
            self._lib.Multiply.restype = ctypes.c_int
            
        if hasattr(self._lib, 'Fibonacci'):
            self._lib.Fibonacci.argtypes = [ctypes.c_int]
            self._lib.Fibonacci.restype = ctypes.c_int
            
        if hasattr(self._lib, 'IsPrime'):
            self._lib.IsPrime.argtypes = [ctypes.c_int]
            self._lib.IsPrime.restype = ctypes.c_int


# Global library loader instance
_loader = _LibraryLoader()


def _get_library():
    """Get the loaded library instance."""
    return _loader.load_library()


def get_quick_replies(token: str, org: str, group: str) -> str:
    """
    Get quick replies from HeyBanco API.
    
    Args:
        token: Authorization token for the API
        org: Organization identifier
        group: Group identifier
        
    Returns:
        JSON string containing the quick replies response
        
    Raises:
        LibCoreHeyError: If the library fails to load or API call fails
    """
    lib = _get_library()
    
    token_bytes = token.encode('utf-8')
    org_bytes = org.encode('utf-8')
    group_bytes = group.encode('utf-8')
    
    try:
        result_ptr = lib.GetQuickReplies(token_bytes, org_bytes, group_bytes)
        if result_ptr:
            result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
            return result
        else:
            return ""
    except Exception as e:
        raise LibCoreHeyError(f"Failed to get quick replies: {e}")


def get_typification(token: str, org: str, group: str) -> str:
    """
    Get typifications from HeyBanco API.
    
    Args:
        token: Authorization token for the API
        org: Organization identifier
        group: Group identifier
        
    Returns:
        JSON string containing the typification response
        
    Raises:
        LibCoreHeyError: If the library fails to load or API call fails
    """
    lib = _get_library()
    
    token_bytes = token.encode('utf-8')
    org_bytes = org.encode('utf-8')
    group_bytes = group.encode('utf-8')
    
    try:
        result_ptr = lib.GetTypification(token_bytes, org_bytes, group_bytes)
        if result_ptr:
            result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
            return result
        else:
            return ""
    except Exception as e:
        raise LibCoreHeyError(f"Failed to get typification: {e}")


def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
        
    Raises:
        LibCoreHeyError: If the library fails to load or function is not available
    """
    lib = _get_library()
    
    if not hasattr(lib, 'Add'):
        raise LibCoreHeyError("Add function not available in library")
    
    try:
        return int(lib.Add(a, b))
    except Exception as e:
        raise LibCoreHeyError(f"Failed to add numbers: {e}")


def multiply_numbers(a: int, b: int) -> int:
    """
    Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
        
    Raises:
        LibCoreHeyError: If the library fails to load or function is not available
    """
    lib = _get_library()
    
    if not hasattr(lib, 'Multiply'):
        raise LibCoreHeyError("Multiply function not available in library")
    
    try:
        return int(lib.Multiply(a, b))
    except Exception as e:
        raise LibCoreHeyError(f"Failed to multiply numbers: {e}")


def get_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n: Position in Fibonacci sequence (must be >= 0)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        LibCoreHeyError: If the library fails to load or function is not available
        ValueError: If n < 0
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    lib = _get_library()
    
    if not hasattr(lib, 'Fibonacci'):
        raise LibCoreHeyError("Fibonacci function not available in library")
    
    try:
        return int(lib.Fibonacci(n))
    except Exception as e:
        raise LibCoreHeyError(f"Failed to calculate Fibonacci: {e}")


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n: Number to check (must be >= 2)
        
    Returns:
        True if n is prime, False otherwise
        
    Raises:
        LibCoreHeyError: If the library fails to load or function is not available
        ValueError: If n < 2
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    
    lib = _get_library()
    
    if not hasattr(lib, 'IsPrime'):
        raise LibCoreHeyError("IsPrime function not available in library")
    
    try:
        return lib.IsPrime(n) != 0
    except Exception as e:
        raise LibCoreHeyError(f"Failed to check if number is prime: {e}")