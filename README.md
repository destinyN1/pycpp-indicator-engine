# pycpp-indicator-engine

A small learning project focused on integrating **C++ and Python** for numerical computation.

The goal of this repository is to build a simple technical indicator engine in **C++** (e.g. moving averages, rolling statistics) and expose it to **Python** for use in a lightweight backtesting workflow. Python is used for data handling, strategy logic, and validation, while C++ is used where performance matters.

This project is intentionally minimal and educational, with an emphasis on:
- Writing clear, modern C++ for numerical algorithms
- Structuring a small C++ library with CMake
- Calling C++ from Python using `pybind11`
- Validating and benchmarking C++ code against Python reference implementations

## Planned features
- Python reference implementations of basic indicators (SMA, EMA)
- C++ implementations of the same indicators
- Python ↔ C++ bindings via `pybind11`
- Simple backtesting loop and performance comparison
- Basic tests to ensure correctness

## Status
🚧 Work in progress — repository initialized, implementation starting soon.

## Motivation
This project is primarily a learning exercise to refresh and deepen understanding of:
- Modern C++ fundamentals
- Python/C++ interoperability
- Performance-aware numerical programming

It is not intended to be a full-featured trading or quant framework.
