# TopstepX 50K multi-asset research v3

## Objective and edit scope
Discover causal OHLCV trading rules for ONE shared simulated $50,000 account, not independent accounts per market. Edit only `strategy.py`. Never alter evaluators, instrument specifications, launcher, quota ledger or sandbox. Research only; no live orders, broker credentials, data purchases or external datasets.

## Available markets
Equity: ES MES NQ MNQ YM MYM RTY M2K NKD.
Energy: CL MCL QM NG MNG QG RB HO.
Metals: GC MGC SI SIL HG MHG PL.
FX: 6E M6E 6B M6B 6A M6A 6C 6J 6S 6N 6M.
Crypto: MBT MET.
Rates: ZB UB ZT ZF ZN TN.
Agriculture: ZC ZS ZW ZL HE LE.
Only use instruments actually present in development cache; history starts at each contract's actual availability. No synthetic MNQ before 2019. Different denominations of one underlying are not independent evidence. Inspect broad universe; simulations may select smaller symbol subsets to bound RAM. No obligation to trade NQ/MNQ.

## Data and partitions
All stages use Databento **1-minute OHLCV**, UTC bar-start timestamps. A completed bar's features become available at its close. No same-bar fills. Decisions can fill the immediately following minute's open only. Every column at every row must be causal, including cross-market alignment.
Development: 2010-06 through 2023-12. Agent-visible files only `/data/dev/<SYMBOL>.parquet`.
Validation: 2024-01 through 2025-08. Not mounted in research environment. Only isolated validator can read it.
Historical final audit: 2025-09 through 2026-08. This period was used in v1/v2; it is **not fresh independent OOS**, regardless of v3 agent memory. No agent access. Final evaluation owner-only after candidate freeze.
Raw data, old task histories, host memories and hidden periods are prohibited. Never infer or request their contents. Latest historical audit is a reused-data check, not proof of live profitability.

## Strategy contract
`signals(panel)` takes `{symbol: pandas.DataFrame}` and returns `{symbol: integer target array}` with one value per input row. Omitted symbols mean flat. Each position is a real integer contract count, never fractional sleeves. Inputs contain OHLCV, contract identifier, CME session label and CT clock seconds. Use explicit trailing windows and lagged cross-market features. No future shift, centered rolling, full-sample normalization, date/month/year/weekday selection or fixed historical timestamp gates. Session clocks are permitted for trading hours. Prefix checks are necessary, not proof against selection bias.
Same rule may use market metadata such as tick size and point value. Explain economic reason for symbol-specific choices; no giant per-symbol tuned parameter table. Maximum six independent entry gates. Risk target at most $300 per new trade based on causal stop distance and dollar point value. Aggregate exposure must remain within evaluator cap. No Kelly estimates from selected backtest wins. ATR scaling permitted, not guaranteed edge.

## Simulation and score
Trusted evaluator is mounted read-only at `/opt/v3-eval`. Use its CLI documented in README. All markets share account PnL, daily lock, trailing loss and exposure. Costs are estimates with stressed slippage and commissions, not official broker fee quotes. A single OHLC minute does not resolve stop/target ordering; evaluator uses documented conservative treatment consistently across all stages. Inspect per-year and per-market reports, turnover, contract counts, entry times and true fill ledger rather than headline score alone.
Do not deliberately fragment trades to satisfy time-diversity checks. No more than 40% of new entries in 08:30–09:30 CT. Do not force trades in five markets merely to manufacture diversification. Report class concentration and correlated exposure.
Null/randomized benchmarks are diagnostics: 200 seeds for frozen finalists. A chosen 95th percentile is not a multiple-testing-adjusted significance guarantee. Do not claim benchmark passed unless executed and recorded.

## Experiment budget and collaboration
At most **30 development experiments per agent**, including unsuccessful changes and crashes. No unrecorded grid/random parameter sweeps. Append each experiment's hypothesis, source SHA256, symbols, score and outcome to `experiments.jsonl`; do not reset it on restart. Share development findings only. Record mechanism and number of variants tried. Inspect failures, not only winners.
Use `hive feed claim` before work. Commit only strategy and permitted experiment notes. `hive push`, then `hive run submit -m DESCRIPTION --score SCORE --parent SHA_OR_none --tldr SUMMARY`. Scores are self-reported until independently reproduced. Do not adopt another candidate without reproducing development result.

## Sealed validation
Freeze and rank up to THREE distinct candidate source files per agent using development evidence, before requesting validation. Owner-provisioned identity determines quota; new source hash is not a new quota. Service computes SHA256 itself. One execution per candidate source hash per agent, **three accepted reservations total per agent**, surviving restarts and concurrent calls. Reservation consumes quota even if code crashes or times out. No new identities to evade quota.
Submit `python3 /usr/local/bin/v3-validate --strategy strategy.py --symbols SYMBOLS` from sandbox. Receipt reports submission/quota state only. Validation metrics, code stdout, errors and per-date traces stay owner-only until research ends. Never tune against service timing, errors or results. No endpoint exposes final audit data.
After 30 development experiments, freeze finalists, submit at most three, save mechanism notes, create `.hive/research-complete`, post completion and exit. Do not continue searching while waiting for validation outcomes.
