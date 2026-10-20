# Lab 14 — Portfolio Baselines

## Rerun Lab 13

`python mandate.py` reran successfully. Candidates A and D pass every checkable rule; B fails the reserve, liquidity, and issuer rules; C fails the reserve rule.

## Diversification

Diversification combines exposures that do not move perfectly together. When correlation is below +1, one sleeve's movement can partly offset another's, lowering the combined portfolio's volatility. It reduces diversifiable issuer-specific risk, but cannot remove market-wide risk; historical correlations can also change, especially in stress periods.

For the 40% investment-grade bond and 60% global-equity benchmark:

- Expected return = 0.40 × 5.0% + 0.60 × 8.0% = 6.80%.
- Bond–equity covariance = 0.25 × 0.06 × 0.16 = 0.0024.
- Variance = (0.40² × 0.06²) + (0.60² × 0.16²) + (2 × 0.40 × 0.60 × 0.0024) = 0.010944.
- Volatility = √0.010944 = 10.46%.

Leaving out the covariance term would incorrectly give 9.90%.

## Validation

`python portfolio.py` should reproduce the course known answers. `mandate.py` includes candidate E, the 40% investment-grade bond / 60% global-equity benchmark; it fails the 3.0% reserve rule because its reserve-eligible weight is 0.0%.

## Reflection

Inverse volatility heavily weights Treasury bills because their 0.5% volatility gives them the largest reciprocal-volatility value. I would show the CIO the benchmark first: it clears the 6.5% return objective and provides the familiar reference allocation, while the mandate checker makes its 0.0% reserve failure explicit.
