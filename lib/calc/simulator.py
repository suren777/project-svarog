import numpy as np
import pandas as pd

dt = 1.0 / 252


def generate_brownian_motion(vol, mean, nsim, nstep):
    noise = np.random.randn(nstep, nsim) * vol * np.sqrt(dt) + mean
    return pd.DataFrame(np.exp(np.cumsum(noise, axis=0, dtype=float)))
