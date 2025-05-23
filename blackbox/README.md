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

Install the required testing tool (tox):

```bash
pip install tox
```

## Running Tests

### Automated Testing with tox

To automatically run tests on Python 3.6, 3.7, 3.8, 3.10, and 3.11:

```bash
tox
```

### Manual Testing for Python 3.5

For Python 3.5, run the following command manually:

For Linux:

```bash
python3.5 pickle_test_runner_py35.py
```

For Window:

```bash
py -3.5 pickle_test_runner_py35.py
```

## File Structure

- `Data/`: Contains black-box test data
- `Linux/`: Stores output results generated in Linux environment
- `Windows/`: Stores output results generated in Windows environment

## Comparing Outputs

To compare output results between different operating systems:

```bash
python compare_hash_outputs.py
```

## Support

If you encounter any issues, please open an issue in this repository.
