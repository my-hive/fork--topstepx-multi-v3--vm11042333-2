"""vm11042333-2: MNQ session trend hold.

Mechanism: equity-index risk premium plus slow trend persistence. On the
09:29 CT bar close (fill 09:30, after cash-open auction) take side = sign(prior session close
- SMA of last TREND_N session closes) (min 20 sessions warmup). Exit on close
beyond stop, close beyond TP_R x stop, data gap (evaluator flattens; no
re-entry churn) or evaluator 15:10 flat. One entry per session.
Stop = STOP_ATR x trailing 20-session mean high-low range (completed sessions
only). Contracts = floor($300 / stop$); if <1 fits, 1 contract, stop = $300.
Tight stop is deliberate: Combine target needs daily variance; edge is small.
"""
import numpy as np
import numba

TRADE = {'MNQ': 2.0}          # symbol: dollars per point
RISK, STOP_ATR, ATR_N, TP_R, TREND_N = 300.0, 0.15, 20, 6.0, 200
ENTRY_SEC = 34140             # signal on 09:29 bar close => fills 09:30 open (US cash open)


@numba.njit(cache=True)
def _run(h, l, c, sec, ts, starts, pv):
    n = len(c)
    out = np.zeros(n, np.int64)
    ns = len(starts) - 1
    rng = np.full(ns, np.nan)
    close = np.full(ns, np.nan)
    for t in range(ns):
        a, b = starts[t], starts[t + 1]
        rng[t] = h[a:b].max() - l[a:b].min()
        close[t] = c[b - 1]
        if t < ATR_N:
            continue
        atr = rng[t - ATR_N:t].mean()   # completed prior sessions only
        ma = close[max(0, t - TREND_N):t].mean()
        d = 1  # long-only control: equity premium without trend side
        if d == 0:
            continue
        stop = STOP_ATR * atr
        q = int(RISK // (stop * pv))
        if q < 1:
            q, stop = 1, RISK / pv
        pos, done, ref = 0, False, 0.0
        for k in range(a, b):
            if k > a and ts[k] - ts[k - 1] != 60:
                pos, done = 0, True        # data gap: evaluator flattened
            if not done:
                if pos == 0 and sec[k] == ENTRY_SEC:
                    pos, ref = d * q, c[k]     # fills next open; levels off signal close
                elif pos != 0 and ((c[k] - ref) * d <= -stop or (c[k] - ref) * d >= TP_R * stop):
                    pos, done = 0, True
            out[k] = pos
    return out


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        if symbol not in TRADE:
            continue
        sid = df.session.to_numpy().astype('int64')
        starts = np.r_[0, np.flatnonzero(np.diff(sid)) + 1, len(sid)].astype(np.int64)
        result[symbol] = _run(df.high.to_numpy(float), df.low.to_numpy(float), df.close.to_numpy(float),
                              df.ct_sec.to_numpy().astype(np.int64), df.index.as_unit('s').asi8, starts, TRADE[symbol])
    return result
