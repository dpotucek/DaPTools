# DaPTools
Personal tools for Python programming - comprehensive utility library

## Installation
```bash
# Install from wheel
pip install dist/daptools-1.1.0-py3-none-any.whl

# Development install
poetry install
```

## Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/testMyTools.py
```

## Modules

### binUtils
Routines for manipulation and formatting of bytes
- `bytes2bin()`, `bin2bytes()`, `bin2dec()`, `dec2bin()`

### cleanDir
Cleans given directory of *.aux, *.log, *.gz produced by LaTeX
- `filter_files()` - filters LaTeX auxiliary files

### fileHasher
File name arbitrary sorter and hasher
- `hash_names()`, `strip_first_alphanumeric()`

### generateSHA
Generates different hashes, compares files with provided signature
- `get_hashsums()`, `create_hash()`, `validate_file()`

### LaTeXHelper
Helper for generating LaTeX entities
- `generate_table_row()` - creates LaTeX table rows

### logger
Simple logging class
- `DataLoger` class for event logging

### mathPhys
Math constants, temperature translation, deg/rad processing
- `deg2rad()`, `rad2deg()`, `c2f()`, `f2c()`, `fibonacci()`

### myTools
Various useful methods (UI for CLI, file & dir works)
- `tree_walker()`, `convert_in_2_mm()`, `num_usr_in()`

### randomPasswordGen
Generates random strong passwords
- `generate_paswd()` - creates random passwords

### sphericalGeodesy
Spherical geodetic calculations
- Distance and bearing calculations

### standardAtmosphere
1976 NASA standard atmosphere model to height 84 km
- Atmospheric properties calculations

### unitsBatch
Converts inches in textual representation to millimeters
- `parse_fraction()`, `parse_number()` - handles fractions

### velikonoce
Easter dates calculations
- `velikonoce` class for Easter date computation

## Build & Distribution
```bash
# Build wheel
poetry build

# Version bump
poetry version patch  # or minor, major
```

## Test Coverage
- 15 comprehensive unit tests
- 11/15 tests fully functional
- Coverage for all major modules