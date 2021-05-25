import numpy as np
import pandas as pd
import argparse
import time
import pickle


class Brownian:
    """
    A Brownian motion class constructor
    """

    def __init__(self, x0=0, seed_value="COIN"):
        """
        :param x0: initial point of brownian motion
        :param n_step: max time step of simulation brownian motion
        :param seed_value: seed value for numpy random
        """
        assert type(x0) == float or type(x0) == int or x0 is None

        self.x0 = float(x0)
        self.seed_int = int(sum([ord(c) for c in seed_value]))

    def gen_normal(self, n_step=100):
        """
        Generate motion by drawing from the Normal distribution

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        if n_step < 30:
            print(
                "WARNING! The number of steps is small. It may not generate a good stochastic process sequence!"
            )

        np.random.seed(self.seed_int)

        w = np.ones(n_step) * self.x0

        for i in range(1, n_step):
            # Sampling from the Normal distribution
            yi = np.random.normal()
            # Weiner process
            w[i] = w[i - 1] + (yi / np.sqrt(n_step))

        return w

    def stock_price(self, s0=100, mu=0.2, sigma=0.62, deltaT=60):
        """
        Models a stock price S(t) using the Weiner process W(t) as
        `S(t) = S(0).exp{(mu-(sigma^2/2).t)+sigma.W(t)}`

        Arguments:
            s0: Iniital stock price, default 100
            mu: 'Drift' of the stock (upwards or downwards), default 1
            sigma: 'Volatility' of the stock, default 1
            deltaT: The time period for which the future prices are computed, default 52 (as in 52 weeks)

        Returns:
            s: A NumPy array with the simulated stock prices over the time-period deltaT
        """
        n_step = int(deltaT)
        time_vector = np.linspace(0, deltaT, num=n_step)
        # Stock variation
        stock_var = (mu - (sigma ** 2 / 2)) * time_vector
        # Weiner process (calls the `gen_normal` method)
        weiner_process = sigma * self.gen_normal(n_step)
        # Add two time series, take exponent, and multiply by the initial stock price
        s = s0 * (np.exp(stock_var + weiner_process))

        return s


def run_brownian(max_round):
    # read csv for table data
    df = pd.read_csv("wishlist.csv")

    # define brownians. not efficient but small people will play
    for i in range(max_round):
        coin_brownian_all = {}
        for coin_name in df.loc[:, "coin"]:
            coin_brownian_all[coin_name] = Brownian(seed_value=coin_name).stock_price(
                deltaT=max_round
            )[: (i + 1)]

        # save brownian temp result
        with open("coin_brownian.pickle", "wb") as f:
            pickle.dump(coin_brownian_all, f, pickle.HIGHEST_PROTOCOL)

        # sleep for lazy run
        if i > 0:
            time.sleep(20)


if __name__ == "__main__":
    # prepare argparse
    parser = argparse.ArgumentParser(description="Args of dash")
    parser.add_argument("--max_round", type=int, default=60)
    args = parser.parse_args()
    max_round = args.max_round

    # run saving brownian results
    run_brownian(max_round)
