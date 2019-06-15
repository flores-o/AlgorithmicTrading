import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from strategies.run_zipline import run_strategy


def main():
    print("*** PackPub - Hands-on Machine Learning for Algorithmic Trading Bots ***")
    print(" BUILD THE CONV BUY AND HOLD STRATEGY")
    perf = run_strategy("auto_correlation")
    perf.to_csv("auto_correlation.csv")


if __name__ == '__main__':
    main()