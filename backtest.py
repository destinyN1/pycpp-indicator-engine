import strategy
import load_data
import numpy as np

#compute simple return from price series
def compute_simple_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        simple_return = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(simple_return)
    return returns

#compute log return from price series
def compute_log_returns(prices):
    import math
    log_returns = []
    for i in range(1, len(prices)):
        log_return = math.log(prices[i] / prices[i-1])
        log_returns.append(log_return)


    return log_returns

def addup_simmple_returns(returns):
    total_return = 0
    for r in returns:
        total_return += r
    return total_return

def addup_log_returns(returns):
    total_return = 0
    for r in returns:
        total_return += r
    return total_return

#compute position array based on signals ("BUY", "SELL", "HOLD")
def compute_positions(signals):
    positions = []
    current_position = 0  # 1 = long, -1 = short, 0 = flat

    for signal in signals:
        if signal == "BUY":
            current_position = 1
            positions.append(current_position)
        elif signal == "SELL":
            current_position = -1
            positions.append(current_position)
        elif signal == "HOLD":
            positions.append(0)  # indicator only, does NOT change state

    return positions

def plot_positions_over_time(positions, title="Positions Over Time"):
    import numpy as np
    import matplotlib.pyplot as plt

    positions = np.asarray(positions)

    # Build a clean state series:
    # - 2 means "HOLD indicator" in your output, not an actual position.
    #   So we carry forward the last real state.
    state = np.empty_like(positions, dtype=int)
    last_state = 0

    for i, p in enumerate(positions):
        if p == 2:
            state[i] = last_state
        else:
            state[i] = int(p)
            last_state = state[i]

    # Plot as a step function (much clearer for positions)
    plt.figure(figsize=(14, 5))
    plt.step(range(len(state)), state, where="post", label="Position (state)")

    # Optional: show HOLD indicators as small dots along the baseline
    hold_idx = np.where(positions == 2)[0]
    if hold_idx.size > 0:
        plt.scatter(hold_idx, np.zeros_like(hold_idx), s=10, label="HOLD (indicator)")

    plt.yticks([-1, 0, 1], ["Short (-1)", "Flat (0)", "Long (1)"])
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time index")
    plt.ylabel("Position")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def compute_equity_curve(prices, positions, initial_capital=1000.0):
    equity = [initial_capital]

    n = min(len(prices), len(positions))  # align lengths
    for i in range(1, n):
        ret = (prices[i] - prices[i-1]) / prices[i-1]
        position = positions[i-1]  # now guaranteed valid
        equity.append(equity[-1] * (1 + ret * position))

    return equity

def plot_equity_curve(equity, title=None):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    from scipy.interpolate import make_interp_spline

    equity = np.asarray(equity, dtype=float)

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=100)

    # Create smooth curve using spline interpolation
    x = np.arange(len(equity))
    
    # Use spline interpolation for smoothness
    # k=3 gives cubic spline (smooth curves)
    if len(equity) > 3:  # Need at least 4 points for cubic spline
        x_smooth = np.linspace(x.min(), x.max(), len(equity) * 10)
        spl = make_interp_spline(x, equity, k=3)
        equity_smooth = spl(x_smooth)
    else:
        x_smooth = x
        equity_smooth = equity

    # Line with antialiasing for smooth rendering
    ax.plot(x_smooth, equity_smooth, linewidth=2, antialiased=True)

    # Only horizontal dashed gridlines
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.45)
    ax.grid(False, axis="x")

    # Nice y-axis ticks + comma formatting (e.g., 350,000)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=12))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{int(x):,}"))

    # Keep the plot clean: no top/right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Minimal labels (the example has no labels)
    if title:
        ax.set_title(title)

    ax.set_xlabel("")  # match screenshot (no x label)
    ax.set_ylabel("")  # match screenshot (no y label)

    # Optional: small margins so the line doesn't touch edges
    ax.margins(x=0.01, y=0.05)

    plt.tight_layout()
    plt.show()


    

if __name__ == "__main__":
    #import sma and ema signals
    sma_signals = np.load('./sma_signals.npy')
    ema_signals = np.load('./ema_signals.npy')
    #import close prices
    close_prices = np.load('./close_prices.npy')

    #compute positions based on signals
    sma_positions = compute_positions(sma_signals)
    ema_positions = compute_positions(ema_signals)

    equity_sma = compute_equity_curve(close_prices, sma_positions)
    equity_ema = compute_equity_curve(close_prices, ema_positions)
    plot_equity_curve(equity_sma)
    plot_equity_curve(equity_ema)

    #compute simple returns
    sma_simple_returns = compute_simple_returns(close_prices)
    ema_simple_returns = compute_simple_returns(close_prices)

    #compute log returns
    sma_log_returns = compute_log_returns(close_prices)
    ema_log_returns = compute_log_returns(close_prices)

    #add up returns
    total_sma_simple_return = addup_simmple_returns(sma_simple_returns)
    total_sma_log_return = addup_log_returns(sma_log_returns)
    total_ema_simple_return = addup_simmple_returns(ema_simple_returns)
    total_ema_log_return = addup_log_returns(ema_log_returns)
    
    #print total returns for SMA and EMA
    print(f"Total SMA Simple Return: {total_sma_simple_return}")
    print(f"Total SMA Log Return: {total_sma_log_return}")
    print(f"Total EMA Simple Return: {total_ema_simple_return}")
    print(f"Total EMA Log Return: {total_ema_log_return}")

    #plot positions over time
    plot_positions_over_time(sma_positions)
    plot_positions_over_time(ema_positions)