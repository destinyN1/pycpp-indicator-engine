# pycpp-indicator-engine

A small learning project focused on integrating C++ and Python for numerical computation and simple backtesting.

The repository provides Python reference implementations of basic technical indicators (SMA, EMA), CSV data loading helpers, a simple strategy (moving average crossover), and basic backtest utilities. The long-term goal is to implement high-performance C++ versions of the same indicators, expose them to Python via pybind11 and compare performance/accuracy.

Status: Work in progress — Python reference implementations present. C++ implementations, bindings, and tests are planned.

Contents
- `load_data.py` — helpers to read CSVs and save ./close_prices.npy
- `indicators.py` — Python implementations of SMA and EMA plus plotting helpers
- `strategy.py` — moving average crossover signal generator and example plotting
- `backtest.py` — simple functions for returns, equity curve and plotting
- `tests/` — placeholder for tests (add/expand pytest tests here)
- other files (`bench.py`, `bindings.cpp`, `indicator_engine.cpp`, `cli.py`, `stats.py`) are scaffolding/placeholders for future C++ work and tooling

Why this repo
- Learn modern C++ numeric programming patterns
- Expose fast C++ numerical code to Python with pybind11
- Validate C++ implementations against straightforward Python reference code
- Learn simple backtesting and performance comparison techniques

Quick start

1) Create a virtual environment and install minimal dependencies
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install numpy matplotlib
# If you want to run tests later:
pip install pytest
```

2) Prepare input data
- Provide a CSV file of OHLCV-like rows where the close price is in column index 4 (5th column). Example layout:
  timestamp,open,high,low,close,volume
- Example: data/1INCHEUR_1440.csv

3) Create the close prices numpy file
```python
from load_data import create_close_price_array
create_close_price_array("data/1INCHEUR_1440.csv")
# This writes ./close_prices.npy and returns the numpy array
```

4) Run indicators (Python reference)
```python
from indicators import run_indicators
close_prices, sma_fast, sma_slow, ema_fast, ema_slow = run_indicators("data/1INCHEUR_1440.csv")
```

5) Generate signals with the moving average crossover strategy
- Option A: use the example `strategy.py` script (it saves ./sma_signals.npy and ./ema_signals.npy)
```bash
python strategy.py
```
- Option B: call the function directly:
```python
from indicators import run_indicators
from strategy import moving_average_crossover_strategy
cp, sma_f, sma_s, ema_f, ema_s = run_indicators("data/1INCHEUR_1440.csv")
sma_signals = moving_average_crossover_strategy(sma_f, sma_s)
ema_signals = moving_average_crossover_strategy(ema_f, ema_s)
```

6) Backtest the signals (example)
```python
from backtest import compute_positions, compute_equity_curve, plot_equity_curve
import numpy as np
close_prices = np.load("./close_prices.npy")
sma_signals = np.load("./sma_signals.npy", allow_pickle=True)  # saved as strings
positions = compute_positions(sma_signals)
equity = compute_equity_curve(close_prices, positions, initial_capital=1000.0)
plot_equity_curve(equity)
```

What is implemented (Python)
- load_data.create_close_price_array — robust CSV reader that extracts the 5th column and writes `./close_prices.npy`.
- indicators.simple_moving_average — convolution-based SMA (returns a shorter array; users should align lengths when using with price arrays).
- indicators.exponential_moving_average — recursive EMA reference implementation.
- strategy.moving_average_crossover_strategy — generates "BUY", "SELL", "HOLD" signals from a pair of series.
- backtest.* — basic returns, positions, equity curve and plotting helpers.

Planned / TODO
- C++ implementations of indicators (in `indicator_engine.cpp`) with comprehensive tests
- pybind11 bindings (in `bindings.cpp`) to expose C++ indicators to Python
- A CLI (`cli.py`) to run common tasks easily
- Benchmarks and micro-bench scripts (`bench.py`)
- More robust backtesting (transaction costs, position sizing, slippage)
- Unit tests (add pytest tests in `tests/`) and CI integration
- Add a `LICENSE` file (none included currently)

Notes & tips
- SMA computed by convolution will produce a shorter array (mode='valid'). When comparing/plotting with original close price arrays you will need to align indices.
- The current CSV loader expects the close price at column index 4 (0-based). Adapt as needed for other CSV formats.
