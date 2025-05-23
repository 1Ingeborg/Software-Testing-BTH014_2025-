# Project Testing Guide

This document provides instructions for setting up the testing environment and running tests for this project.

## Prerequisites

Before running the tests, please ensure you have the following Python versions installed:

- Python 3.5
- Python 3.6
- Python 3.7
- Python 3.8
- Python 3.10
- Python 3.11

## Installation

Install the required testing tools:

```bash
pip install coverage
```

## Running Tests

### Whitebox Testing

Run whitebox tests for each Python version:

**On Windows:**
```bash
py -3.5 pickle_hash_whitebox.py
py -3.6 pickle_hash_whitebox.py
py -3.7 pickle_hash_whitebox.py
py -3.8 pickle_hash_whitebox.py
py -3.10 pickle_hash_whitebox.py
py -3.11 pickle_hash_whitebox.py
```

**On Linux:**
```bash
python3.5 pickle_hash_whitebox.py
python3.6 pickle_hash_whitebox.py
python3.7 pickle_hash_whitebox.py
python3.8 pickle_hash_whitebox.py
python3.10 pickle_hash_whitebox.py
python3.11 pickle_hash_whitebox.py
```

### Comparing Outputs

To compare binary stream differences between versions:

```bash
python pickle_compare.py
```

## File Structure
- `outputs/`: Directory for saving binary stream results

## Key Files

- `pickle_hash_whitebox.py`: Whitebox testing script
- `pickle_compare.py`: Script for comparing binary stream differences
- `testdata.py`: Contains test datasets and methods

> Note: `creatRandom.py` is deprecated and should be ignored.

## Support

If you encounter any issues, please open an issue in this repository.
