# if TYPE_CHECKING:
from numbers import Integral
from typing import Set

import matplotlib.lines
import numpy as np
from matplotlib.artist import allow_rasterization
from matplotlib.axes import Axes
from matplotlib.backend_bases import RendererBase

__all__ = [
    "DataSource",
    "SimpleSource",
    "DFSource",
    "FuncSource1D",
    "ArraySource1D",
    "DSLine2D",
    "InvalidDataSource",
]


class InvalidDataSource(ValueError):
    ...


class DataSource:
    def get(self, keys: Set[str], ax: Axes, renderer: RendererBase):
        raise NotImplementedError


class SimpleSource(DataSource):
    def __init__(self, **kwargs):
        self._data = {k: np.asanyarray(v) for k, v in kwargs.items()}
        self.md = {k: {"ndim": v.ndim, "dtype": v.dtype} for k, v in self._data.items()}

    def get(self, keys, ax=None, renderer=None):
        return {k: self._data[k] for k in keys}


# TODO: add some typing here
class DFSource(DataSource):
    def __init__(self, df, **kwargs):
        self._remapping = kwargs
        self._data = df
        self.md = {k: {"ndim": 1, "dtype": df[v].dtype} for k, v in kwargs.items()}

    def get(self, keys, ax, renderer):
        return {k: self._data[self._mapping[k]] for k in keys}


class FuncSource1D(DataSource):
    def __init__(self, func):
        self._func = func
        self.md = {"x": {"ndim": 1, "dtype": float}, "y": {"ndim": 1, "dtype": float}}

    def get(self, keys, ax, renderer):
        assert set(keys) == set(self.md)
        xlim = ax.get_xlim()
        bbox = ax.get_window_extent(renderer)
        xpixels = bbox.width
        x = np.linspace(*xlim, xpixels)
        return {"x": x, "y": self._func(x)}


class ArraySource1D(DataSource):
    def __init__(self, array, scale=1) -> None:
        self._arr = array
        self._scale = scale
        # TODO: also account for xarray?
        if hasattr(self._arr, "vindex"):
            # accounting for zarr
            self._indexer = self._arr.vindex
        else:
            self._indexer = self._arr
        self.md = {"x": {"ndim": 1, "dtype": float}, "y": {"ndim": 1, "dtype": float}}

    @property
    def scale(self) -> int:
        return self.scale

    @scale.setter
    def scale(self, value: int):
        if not isinstance(value, Integral):
            raise TypeError(f"scale must be integer values but is type {type(value)}")
        self._scale = value

    def get(self, keys: Set[str], ax: Axes, renderer):
        xlim = ax.get_xlim()
        xmin = np.max([int(xlim[0]), 0])
        xmax = np.min([np.max([int(xlim[1]), -1]), self._arr.shape[0]])
        x = np.arange(xmin, xmax, self._scale)

        return {"x": x, "y": self._indexer[x]}


class DSLine2D(matplotlib.lines.Line2D):
    def __init__(self, DS, **kwargs):
        if not all(k in DS.md for k in ("x", "y")):
            raise InvalidDataSource
        self._DS = DS
        super().__init__([], [], **kwargs)

    @allow_rasterization
    def draw(self, renderer):
        data = self._DS.get({"x", "y"}, self.axes, renderer)
        super().set_data(data["x"], data["y"])

        return super().draw(renderer)
