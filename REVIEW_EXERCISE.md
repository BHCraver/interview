# Code Review Exercise (~30 minutes)

Welcome. This repo is a small service, **`delay-risk`**, that scores a flight's risk of
arriving late. A teammate has opened a pull request — **DR-142** (see the **Pull requests** tab)
— and asked you to review it before it merges.

Please review it the way you would any PR from a colleague.

## What we'd like from you
1. Walk us through your review out loud — what you notice, in the order you'd raise it.
2. Give a clear verdict: **approve**, **request changes**, or **block** — and why.
3. Prioritize: what *must* be fixed before merge vs. what's a minor note.
4. Toward the end, we'll ask: **what modeling approach would you use for this problem, and why?**

There's no single "right answer" — we're interested in how you reason about code quality,
design, and modeling choices, and how you'd communicate the feedback to the author.

## The request that prompted the PR
See [`TICKET.md`](./TICKET.md) (DR-142). In short: *make the delay-risk score more accurate than
the current linear baseline, keep the public contract stable, keep it deterministic, and show it
beats the baseline on the labeled sample.*

## How to look at the change
- Read the PR: its description and the **Files changed** tab on GitHub.
- Or locally:
  ```bash
  git clone <this-repo> && cd interview
  git diff main..dr-142-neural-model     # the change under review

  python -m pytest -q                    # tests
  python eval/backtest.py                # accuracy on the labeled sample (data/flights_sample.csv)
  ```
You're welcome to run things — read files, run the tests, run the backtest, poke at inputs.

Get oriented with the baseline first (`src/delay_risk/predict.py`, `README.md`, `TICKET.md`),
then dig into the PR.
