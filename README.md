# LibCoreHey

Python wrapper for HeyBanco's core Go library, providing easy access to HeyBanco APIs and utility functions.

## Features

- 🏦 **HeyBanco APIs**: Access to Quick Replies and Typification endpoints
- 🧮 **Math Utilities**: Basic mathematical operations (add, multiply, fibonacci, prime checking)
- 🚀 **High Performance**: Built with Go for optimal performance
- 🐍 **Pythonic Interface**: Clean and intuitive Python API
- 🔒 **Type Safe**: Full type hints support
- 📦 **Easy Installation**: Simple pip install

## Installation

### From PyPI (Recommended)

```bash
pip install LibCoreHey
```

### From Source

```bash
git clone https://github.com/betoebaez/PoC-GoLib.git
cd PoC-GoLib
pip install -e .
```

**Prerequisites:**
- Python 3.8+
- **No Go compiler needed** - Uses pre-built binaries!

**Note:** This package includes pre-compiled binaries for macOS, Linux, and Windows. No additional dependencies required!

## Quick Start

```python
import libcorehey as LibCoreHey

# HeyBanco API calls
token = "your-api-token"
org = "your-org"
group = "your-group"

# Get quick replies
replies = LibCoreHey.get_quick_replies(token, org, group)
print(replies)

# Get typifications
typifications = LibCoreHey.get_typification(token, org, group)
print(typifications)

# Math utilities
result = LibCoreHey.add_numbers(5, 3)  # Returns 8
product = LibCoreHey.multiply_numbers(4, 6)  # Returns 24
fib = LibCoreHey.get_fibonacci(10)  # Returns 55
is_prime = LibCoreHey.is_prime(17)  # Returns True
```

## API Reference

### HeyBanco APIs

#### `get_quick_replies(token: str, org: str, group: str) -> str`

Retrieves quick replies from HeyBanco API.

**Parameters:**
- `token`: Authorization token for the API
- `org`: Organization identifier
- `group`: Group identifier

**Returns:** JSON string containing the quick replies response

**Example:**
```python
import libcorehey as LibCoreHey

replies = LibCoreHey.get_quick_replies("your-token", "your-org", "your-group")
print(replies)
```

#### `get_typification(token: str, org: str, group: str) -> str`

Retrieves typifications from HeyBanco API.

**Parameters:**
- `token`: Authorization token for the API
- `org`: Organization identifier  
- `group`: Group identifier

**Returns:** JSON string containing the typification response

**Example:**
```python
import libcorehey as LibCoreHey

typifications = LibCoreHey.get_typification("your-token", "your-org", "your-group")
print(typifications)
```

### Math Utilities

#### `add_numbers(a: int, b: int) -> int`

Adds two numbers.

**Parameters:**
- `a`: First number
- `b`: Second number

**Returns:** Sum of a and b

#### `multiply_numbers(a: int, b: int) -> int`

Multiplies two numbers.

**Parameters:**
- `a`: First number
- `b`: Second number

**Returns:** Product of a and b

#### `get_fibonacci(n: int) -> int`

Calculates the nth Fibonacci number.

**Parameters:**
- `n`: Position in Fibonacci sequence (must be >= 0)

**Returns:** The nth Fibonacci number

**Raises:** `ValueError` if n < 0

#### `is_prime(n: int) -> bool`

Checks if a number is prime.

**Parameters:**
- `n`: Number to check (must be >= 2)

**Returns:** True if n is prime, False otherwise

**Raises:** `ValueError` if n < 2

## Error Handling

The library defines a custom exception `LibCoreHeyError` for library-specific errors:

```python
from libcorehey import LibCoreHeyError

try:
    result = LibCoreHey.get_quick_replies("invalid-token", "org", "group")
except LibCoreHeyError as e:
    print(f"API Error: {e}")
except ValueError as e:
    print(f"Input Error: {e}")
```

## Platform Support

- ✅ **macOS** (x64, ARM64)
- ✅ **Linux** (x64, ARM64)
- ✅ **Windows** (x64)

## Development

### Building from Source

1. Clone the repository:
```bash
git clone https://github.com/heybanco/LibCoreHey.git
cd LibCoreHey
```

2. Install Go dependencies and build:
```bash
./build.sh
```

3. Install in development mode:
```bash
pip install -e .
```

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Building Distribution

```bash
python setup.py sdist bdist_wheel
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0 (2025-12-02)
- Initial release
- HeyBanco API integration (Quick Replies, Typification)
- Cross-platform support with GitHub Actions
- Pre-built binaries for macOS, Linux, Windows
- Full type hints support

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/heybanco/LibCoreHey/issues)
- 📚 **Documentation**: [README](https://github.com/heybanco/LibCoreHey/blob/main/README.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/heybanco/LibCoreHey/discussions)

---

**Made with ❤️ by the HeyBanco Team**