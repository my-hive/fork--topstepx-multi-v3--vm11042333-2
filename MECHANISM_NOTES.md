# vm11042333-2 mechanism notes (development only)

## Submitted finalists (MNQ only; validation symbols MNQ)
1. `8403b4f1e486` exp6: MNQ long, signal on 09:29 bar close -> fill 09:30 open,
   hold to 15:09/flat, close-based stop 0.15 x ATR20(session range), TP 6R,
   $300 risk, contracts = floor(300/stop$), gap => flat rest of session.
   Dev score 0.1467 (2019 0, 2020 .248, 2021 .261, 2022 .192, 2023 .249).
   Side-null 200 seeds: p=0.010 (null mean .059, p95 .110).
2. `1b7d98b6d12f` exp7: same, no TP. Dev 0.1147, p=0.030.
3. `6e16cc8b9476` exp4: 17:00 entry, side = sign(prev close - SMA200 sessions).
   Dev 0.0987, no null run.

## What the score is and is not
Score = rolling-30-session Combine pass rate, mean of worst 3 eligible years.
Passing needs +$3000 within 30 sessions => daily PnL sd must be large
(sim: sd 600 => ~25% random-pass baseline). Tight stop (0.15 ATR, ~7-14 MNQ)
manufactures that variance cheaply. Null p-values test side choice only;
timing/long-bias is preserved, so NOT a full significance proof. Net PnL of
exp4 config was ~breakeven after fees: variance, not proven edge.

## Evidence that survived (development, gross of any selection)
- Only cost-surviving drift: NQ/MNQ session long (~+0.05R t~1.4; 2022 bear year negative).
- Everything else negative after stressed costs: TSMOM(20/60/120) daily, session
  reversal, ORB 30m (23 markets), prior-extreme breakout AND fade, 07:30 macro
  shock follow/fade, time-of-day momentum, cross-market overnight leads,
  micro/rates/FX/grains session holds (costR 0.15-0.8 at 0.5ATR stops).
- Stressed cost = 2 ticks slip + 1.5x fee per side; low-cost/ATR ranking:
  NQ .27%, HO .33%, RB .37%, MNQ .42% - MNQ chosen on this, not data mining.

## Caveats for owner
- MNQ 2019 data gappy (17 gaps/session early) -> 2019 rate 0; dev score uses
  worst-3-year mean, so 2019 anchors it. Single-market candidate: family
  concentration = 1 (equity), max exposure 1.4 of 5.
- Development score is not evidence of deployable profitability.
