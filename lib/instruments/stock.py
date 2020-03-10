import numpy as np


class Stock:
    def __init__(self, name, price, rate=None, vol=None):
        self.name = name
        self.value = price
        self.rate = rate
        self.vol = vol

    def simulate_price(self, nSteps=100, dT=1 / 252.0):
        noise = np.random.randn(nSteps) * self.vol * np.sqrt(dT) + self.rate * dT
        noise[0] = 0
        self.prices = self.value * np.exp(np.cumsum(noise, dtype=float))
        return self.prices
