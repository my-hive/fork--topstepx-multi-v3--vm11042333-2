"""vm11042333-2: equity-index session hold (equity risk premium, overnight+day).

Mechanism: index futures earn a risk premium; NQ showed the only cost-surviving
session-level drift in development diagnostics. Enter long at first bar of the
CME session (17:00 CT), exit on close-based stop or evaluator 15:10 flat.
Data gap inside session => flat for rest of session (no re-entry churn).
Stop = STOP_ATR x trailing 20-session mean high-low range (completed sessions
only). Contracts = floor($300 / stop$); if <1 contract fits, 1 contract with
stop shrunk to exactly $300.
"""
import numpy as np
import numba

TRADE = {'MNQ': 2.0}          # symbol: dollars per point
RISK, STOP_ATR, ATR_N = 300.0, 1.0, 20


@numba.njit(cache=True)
def _run(o, h, l, c, sec, ts, starts, pv):
    n = len(o)
    out = np.zeros(n, np.int64)
    ns = len(starts) - 1
    rng = np.full(ns, np.nan)
    for t in range(ns):
        a, b = starts[t], starts[t + 1]
        rng[t] = h[a:b].max() - l[a:b].min()
        if t < ATR_N:
            continue
        atr = rng[t - ATR_N:t].mean()   # completed prior sessions only
        stop = STOP_ATR * atr
        q = int(RISK // (stop * pv))
        if q < 1:
            q, stop = 1, RISK / pv
        pos, sp = 0, 0.0
        for k in range(a, b):
            if k > a and ts[k] - ts[k - 1] != 60:
                pos, sp = 0, -1.0         # data gap: evaluator flattened; stay out rest of session
            if pos == 0 and sp == 0.0 and (sec[k] >= 61200 or sec[k] < 54000):
                pos, sp = q, c[k] - stop   # filled next open; stop ref on signal close
            elif pos > 0 and c[k] <= sp:
                pos = 0
            out[k] = pos
    return out


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        if symbol not in TRADE:
            continue
        sid = df.session.to_numpy().astype('int64')
        starts = np.r_[0, np.flatnonzero(np.diff(sid)) + 1, len(sid)].astype(np.int64)
        result[symbol] = _run(df.open.to_numpy(float), df.high.to_numpy(float), df.low.to_numpy(float),
                              df.close.to_numpy(float), df.ct_sec.to_numpy().astype(np.int64),
                              df.index.as_unit('s').asi8, starts, TRADE[symbol])
    return result
