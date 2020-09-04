import matplotlib.pyplot as plt
import numpy as np

def imagesc(I,ax = None,  x=None, y=None, **kwargs):
    if ax is None:
        plt.figure()
        ax = plt.axes()
    if x is None:
        Nx = np.size(I, axis=1)
        x = np.arange(Nx)
    if y is None:
        Ny = np.size(I, axis=0)
        y = np.arange(Ny)
    ext = (x[0], x[-1], y[-1], y[0])
    return ax.imshow(I, extent=ext, aspect='auto', **kwargs)