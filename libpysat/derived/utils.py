import numpy as np
import warnings

def generic_func(data, wavelengths, kernels={}, func=None, axis=0, pass_wvs=False, **kwargs):
    """
    Using some form of data and a wavelength array. Get the bands associated
    wtih each wavelength in wavelengths, create a subset of bands based off
    of those wavelengths then hand the subset to the function.

    Parameters
    ----------
    data : ndarray
           (x, y, z) 3 dimensional numpy array of a spectra image

    wv_array : iterable
               A list of all possible wavelengths for a given spectral image

    wavelengths : iterable
                  List of wavelengths to use for the function

    Returns
    ----------
    : func
      Returns the result from the given function
    """
    if kernels:
        subset = []
        wvs = data.wavelengths

        for k, v in kernels.items():
            s = sorted(np.abs(wvs-k).argsort()[:v])
            subset.append(np.median(data.iloc[s, :, :], axis=axis))
        if len(subset) == 0:
            subset = subset[0]
    else:
        subset = data.loc[wavelengths, :, :]
    if pass_wvs:
        return func(subset, wavelengths, **kwargs)
    return func(subset, **kwargs)

def warn_m3(m3_func, *args, **kwargs):
    def call_warn(*args, **kwargs):
        warnings.warn('Parameters involving some of the visible wavelengths ( < 600 nm) are not recommended for use. Parameters modeled after Clementine data are also not recommended. Original parameter estimates for OH and H2O should NOT be included.')
        return m3_func(*args, **kwargs)
    return call_warn
