import numpy as np
import matplotlib.pyplot as plt
from scipy.special import exp1 as W


def set_time(t):
    if isinstance(t, (int, float, np.int, np.float)):
        t = np.array([t], dtype=np.float)
    elif isinstance(t, (list, tuple)):
        t = np.array(t, dtype=np.float)
    elif isinstance(t, (str)):
        print("dummy you can't use a string '{}'".format(t))
        return None
    return t


def theis(r, t, Q=1.16, T=0.3, S=0.0008):
    t = set_time(t)
    u = np.zeros(t.shape[0], dtype=np.float)
    mask = t > 0
    u[mask] = ((r ** 2) * S) / (4 * T * t[mask])
    s = (Q / (4 * np.pi * T)) * W(u)
    return s


def radius(pw=(0., 0.), po=(1000., 1000.)):
    return (np.sqrt((pw[0] - po[0]) ** 2 +
                    (pw[1] - po[1]) ** 2))


def theis_array(nrows, t, dx=100., ptw=(0, 0),
                Q = 1.16, T = 0.3, S = .0008):
    ncols = nrows
    t = set_time(t)
    s = np.zeros((t.shape[0], nrows, ncols),
                 dtype=np.float)
    for i in range(nrows):
        for j in range(ncols):
            x = (j + 0.5) * dx
            y = (nrows - i - 0.5) * dx
            r = radius(ptw, (x, y))
            s[:, i, j] = theis(r, t, Q=Q, T=T, S=S)
    return s


if __name__ == "__main__":
    # Can evaluate for a single value
    s = theis(radius(), 86400.)
    print(s)

    # Alternatively, can use a numpy array. Can't use a list.
    t = np.arange(0, 864000., 864.)  # times to evaluate
    print(t)
    s = theis(radius(), t)
    print(s)
    plt.plot(t, s)

    sarray = theis_array(10, [864000, 8640000])
    print(sarray.shape)

    plt.imshow(sarray[0, :, :])
    plt.colorbar()

    plt.imshow(sarray[1, :, :])
    plt.colorbar()
