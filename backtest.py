import strategy
import load_data

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

if __name__ == "__main__":