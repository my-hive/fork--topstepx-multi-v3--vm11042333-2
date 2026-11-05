# TopstepX multi-asset v3

Research task under construction. **Not launch-ready until owner verification passes.**

Read program.md for frozen partitions, candidate limits and safety boundaries. All stages use one-minute OHLCV and the same trusted account evaluator. Historical final block overlaps v1/v2 research and is not fresh OOS.

Only strategy.py is editable. Agent sandbox receives development data at /data/dev and trusted evaluator at /opt/v3-eval. Validator takes source plus selected symbols and returns receipts only. Source must define signals(panel); integer targets, same row count per symbol. Account rules apply jointly across instruments.

Exact evaluator CLI and verified launch procedure will be added after integration tests. Do not launch by copying v2 commands.
