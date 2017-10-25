import pandas as pd
import xarray as xr
import numpy as np

import numpy.testing as npt
import xarray.testing as xrt

from neuroglia.spike import Smoother, Binarizer

from sklearn.base import clone

# create fake spike data
SPIKES = pd.DataFrame({'neuron':[0,0,1],'time':[0.01,0.2,0.83]})

# create bins attribute
TS  = np.arange(0,1,0.01)

def test_Smoother():
    smoother = Smoother(sample_times=TS)
    smoothed = smoother.fit_transform(SPIKES)

    npt.assert_array_equal(smoothed.index,TS)

def test_Binarizer():
    binarizer = Binarizer(sample_times=TS)
    binarized = binarizer.fit_transform(SPIKES)

    npt.assert_array_equal(binarized.index,TS[:-1])

def test_Smoother_noresp():
    smoother = Smoother(sample_times=TS+100.0)
    smoothed = smoother.fit_transform(SPIKES)

    npt.assert_equal(
        smoothed.values,
        np.zeros((len(TS),2),np.float),
        )

def test_Smoother_empty():
    smoother = Smoother(sample_times=TS+100.0)
    empty_spikes = SPIKES[SPIKES['time'].map(lambda x: False)]
    smoothed = smoother.fit_transform(empty_spikes)
    npt.assert_array_equal(smoothed.index,TS+100)


# Test for proper parameter structure
def test_params():
    fn_list = [
        Smoother(sample_times=TS),
        Binarizer(sample_times=TS),
        ]
    for fn in fn_list:
        new_object_params = fn.get_params(deep=False)
        for name, param in new_object_params.items():
            new_object_params[name] = clone(param, safe=False)
