"""Calculate risk and return for the Lab 14 Meridian portfolio baselines."""

from math import sqrt


# Editable course-authored training inputs. Values are decimals, not percentages.
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005, "reserve_eligible": True},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070, "reserve_eligible": True},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060, "reserve_eligible": False},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160, "reserve_eligible": False},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00, "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10, "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05, "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00, "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065


def validate_correlations(correlations, sleeves):
    """Raise ValueError unless the full correlation table is symmetric and valid."""
    names = tuple(sleeves)
    if set(correlations) != set(names):
        raise ValueError("Correlation table must have one row for every sleeve.")
    for left in names:
        if set(correlations[left]) != set(names):
            raise ValueError(f"Correlation row for {left} must have every sleeve.")
        for right in names:
            value = correlations[left][right]
            if not -1 <= value <= 1:
                raise ValueError(f"Correlation for {left} and {right} must be between -1 and 1.")
            if value != correlations[right][left]:
                raise ValueError(f"Correlation table is not symmetric for {left} and {right}.")


def covariance_matrix(sleeves, correlations):
    """Return covariance entries: correlation times the two sleeve volatilities."""
    return {
        left: {
            right: correlations[left][right] * sleeves[left]["volatility"] * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def expected_return(weights, sleeves):
    """Return the weighted expected return."""
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_volatility(weights, covariance):
    """Return sqrt(w' covariance w), including each covariance term."""
    variance = sum(
        weights[left] * weights[right] * covariance[left][right]
        for left in weights
        for right in weights
    )
    if variance < 0:
        raise ValueError("Portfolio variance is negative; check the input correlation table.")
    return sqrt(variance)


def reserve_eligible_weight(weights, sleeves):
    """Return the combined weight of reserve-eligible sleeves."""
    return sum(weights[name] for name in sleeves if sleeves[name]["reserve_eligible"])


def equal_weight_portfolio(sleeves):
    """Return equal weights across all sleeves."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_portfolio(sleeves):
    """Return weights proportional to the reciprocal of each sleeve's volatility."""
    inverse_volatilities = {name: 1 / data["volatility"] for name, data in sleeves.items()}
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def baseline_portfolios(sleeves):
    """Define the three portfolios required by Lab 14."""
    benchmark = {name: 0.0 for name in sleeves}
    benchmark["Investment-grade bond fund"] = 0.40
    benchmark["Global equity index fund"] = 0.60
    return {
        "Benchmark": benchmark,
        "Equal weight": equal_weight_portfolio(sleeves),
        "Inverse volatility": inverse_volatility_portfolio(sleeves),
    }


def format_weights(weights):
    """Return the sleeve weights in the course-table order."""
    return " / ".join(f"{weights[name] * 100:.1f}" for name in SLEEVES)


def print_portfolio(name, weights, sleeves, covariance, objective):
    """Print one baseline's weights, expected return, risk, reserve share, and objective result."""
    portfolio_return = expected_return(weights, sleeves)
    volatility = portfolio_volatility(weights, covariance)
    reserve_weight = reserve_eligible_weight(weights, sleeves)
    meets_objective = "yes" if portfolio_return >= objective else "no"
    print(f"{name}:\n"
          f"  Weights (bills / 10-year / IG / equity): {format_weights(weights)}%\n"
          f"  Expected return: {portfolio_return * 100:.2f}%\n"
          f"  Volatility: {volatility * 100:.2f}%\n"
          f"  Reserve-eligible: {reserve_weight * 100:.1f}%\n"
          f"  Meets {objective * 100:.1f}% objective? {meets_objective}")


def main():
    """Validate inputs and print all baseline results."""
    validate_correlations(CORRELATIONS, SLEEVES)
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    for name, weights in baseline_portfolios(SLEEVES).items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN)
        print()


if __name__ == "__main__":
    main()
