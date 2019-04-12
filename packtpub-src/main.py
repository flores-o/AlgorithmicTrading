import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from strategies.run_zipline import run_strategy


def main():
    print("*** PackPub - Hands-on Machine Learning for Algorithmic Trading Bots ***")
    print(" BUILD THE CONV BUY AND HOLD STRATEGY")
    perf = run_strategy("buy_and_hold")
    perf.to_csv("buy_and_hold.csv")


if __name__ == '__main__':
    main()