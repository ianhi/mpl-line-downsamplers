try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Ian Hunt-Isaak"
__email__ = "ianhuntisaak@gmail.com"

from ._downsamplers import (
    ArraySource1D,
    DataSource,
    DFSource,
    DSLine2D,
    FuncSource1D,
    InvalidDataSource,
    SimpleSource,
)

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "DataSource",
    "SimpleSource",
    "DFSource",
    "FuncSource1D",
    "ArraySource1D",
    "DSLine2D",
    "InvalidDataSource",
]
