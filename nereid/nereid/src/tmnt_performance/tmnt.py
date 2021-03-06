from typing import Any, Callable, Dict, Mapping, Optional, Tuple
from functools import partial
import numpy
import pandas

from nereid.core.units import ureg


def effluent_conc(
    inf_conc: float,
    inf_unit: str,
    A: float = 0,
    B: float = 0,
    e1: float = 0,
    C: float = 0,
    e2: float = 0,
    D: float = 0,
    E: float = 0,
    dl: float = 0,
    unit: Optional[str] = None,
    **kwargs: Dict
) -> float:
    """
    This function applies the NCHRP formula for computing bmp performance using
    a compound curve fitting function defined as:

    effluent = min(inf_conc, max(A + B*inf_conc + C*ln(inf_conc) + D*(inf_conc**E)*e2, dl))

    Parameters
    ----------
    inf_conc : float
    inf_unit : string
        units of the concentration data is passed into the function
        these units be recognizable by the `pint` library
    A : float
    B : float
    e1 : float
    C : float
    e2 : float
    D : float
    E : float
    dl : float
        is the maximum of the minimum reported detection limits
    unit : string, optional (default=None)

    **kwargs : dictionary
        ignored by this function
    """

    if unit is None:
        unit = inf_unit

    inf_conc = inf_conc * ureg(inf_unit).to(unit).magnitude

    eff = inf_conc  # assume no treatment

    # force log(0) to return 0 instead of undefined.
    _C = 0
    if inf_conc > 0:
        _C = C * numpy.log(inf_conc)

    if any([A, B, C, D, E]):
        eff = numpy.nansum([A, B * inf_conc, _C, e1, D * (inf_conc ** E) * e2])

    result: float = numpy.nanmax([dl, numpy.nanmin([eff, inf_conc])])
    result *= ureg(unit).to(inf_unit).magnitude

    return result


def build_effluent_function_map(
    df: pandas.DataFrame, facility_column: str, pollutant_column: str
) -> Mapping[Tuple[str, str], Callable]:
    # this is close to what we want, but it has a lot of nans.
    _bmp_dict = df.set_index([facility_column, pollutant_column]).to_dict("index")

    # this gives a lookup table in the form {(bmp, pollutant) : **args}
    # with no nans.
    bmp_dict = {
        k: {ki: vi for ki, vi in v.items() if pandas.notnull(vi)}
        for k, v in _bmp_dict.items()
    }

    # this gives a lookup table in the form {(bmp, pollutant) : fxn(inf_conc, inf_conc_units)}
    function_map = {k: partial(effluent_conc, **v) for k, v in bmp_dict.items()}

    return function_map
