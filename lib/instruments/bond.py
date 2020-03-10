import numpy as np


class Bond:
    def __init__(self, name, rating="AAA", coupon=0, maturity=1, frequency=1):
        self.name = name
        self.rating = rating
        self.coupon = coupon
        self.maturity = maturity
        self.coupon_frequency = frequency

    def price(self):
        return None
