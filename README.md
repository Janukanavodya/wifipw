# WiFi Password Manager

A simple, secure WiFi password manager written in Python with comprehensive test coverage.

## Features

- **Secure Storage**: Passwords are encrypted using SHA-256 hashing
- **SSID Validation**: Validates WiFi network names according to WiFi standards (1-32 characters)
- **Password Validation**: Ensures passwords meet WPA/WPA2 standards (8-63 characters)
- **Simple CLI**: Easy-to-use command-line interface
- **Comprehensive Testing**: Full test suite with high coverage

## Installation

```bash
# Clone the repository
git clone https://github.com/Janukanavodya/wifipw.git
cd wifipw

# Install testing dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the interactive CLI:

```bash
python wifipw.py
```

Available commands:
- `add` - Add a new WiFi password
- `get` - Retrieve a stored password
- `remove` - Remove a stored password
- `list` - List all stored networks
- `quit` - Exit the program

### Programmatic Usage

```python
from wifipw import WiFiPasswordManager

# Create a manager instance
manager = WiFiPasswordManager()

# Add a password
success = manager.add_password("MyNetwork", "mypassword123")

# Retrieve a password
password = manager.get_password("MyNetwork")

# List all networks
networks = manager.list_networks()

# Remove a password
removed = manager.remove_password("MyNetwork")
```

## Testing

### Run Tests

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run tests with coverage
python -m pytest --cov=wifipw --cov-report=term-missing

# Run tests using Make (if make is available)
make test
make coverage
```

### Test Coverage

The project includes comprehensive tests covering:

- ✅ **Basic Operations**: Add, get, remove, and list passwords
- ✅ **Validation**: SSID and password format validation
- ✅ **Security**: Password encryption and verification
- ✅ **Edge Cases**: Unicode characters, special characters, case sensitivity
- ✅ **Error Handling**: Invalid inputs and missing data

Current test coverage: **62%** (excluding interactive CLI code)

### Test Structure

- `test_wifipw.py` - Main test suite with 25+ test cases
- Tests are organized into logical groups:
  - `TestWiFiPasswordManager` - Core functionality tests
  - `TestSSIDValidation` - SSID format validation tests
  - `TestPasswordValidation` - Password format validation tests
  - `TestPasswordEncryption` - Security and encryption tests
  - `TestEdgeCases` - Edge cases and error conditions

## Development

### Project Structure

```
wifipw/
├── wifipw.py              # Main WiFi password manager
├── test_wifipw.py         # Comprehensive test suite
├── requirements.txt       # Testing dependencies
├── pytest.ini           # Pytest configuration
├── Makefile             # Development commands
├── .github/
│   └── workflows/
│       └── test.yml     # GitHub Actions CI
└── README.md           # This file
```

### Running Development Commands

```bash
# Install dependencies
make install

# Run tests
make test

# Generate coverage report
make coverage

# Clean generated files
make clean

# Show available commands
make help
```

## Security Features

- **Encrypted Storage**: Passwords are never stored in plaintext
- **SHA-256 Hashing**: Industry-standard cryptographic hashing
- **Input Validation**: Prevents invalid SSIDs and passwords
- **Memory Management**: Passwords can be cleared from memory

## WiFi Standards Compliance

- **SSID Length**: 1-32 characters (WiFi standard)
- **Password Length**: 8-63 characters (WPA/WPA2 standard)
- **Character Support**: Full Unicode support within length limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the MIT License.