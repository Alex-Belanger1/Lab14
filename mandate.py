"""Check candidate portfolios against the Meridian Foundation Reserve mandate."""

# Editable inputs
HOLDINGS = {
    "Cash": {
        "issuer": "none",
        "business_days_to_redeem": 0,
        "reserve_eligible": True,
    },
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "business_days_to_redeem": 1,
        "reserve_eligible": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "business_days_to_redeem": 1,
        "reserve_eligible": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 2,
        "reserve_eligible": False,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 3,
        "reserve_eligible": False,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "business_days_to_redeem": 90,
        "reserve_eligible": False,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "business_days_to_redeem": 4,
        "reserve_eligible": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "business_days_to_redeem": 1,
        "reserve_eligible": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    # Deliberately passes the checkable rules while probing the undefined loss rule (S9).
    "D": {
        "Cash": 3,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 97,
        "Investment-grade bond fund": 0,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    # Lab 14's 40% investment-grade bond / 60% global-equity benchmark.
    "E": {
        "Cash": 0,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 40,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5  # business days
MINIMUM_LIQUID_SHARE = 90  # percent
ISSUER_LIMIT = 8  # percent

EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def result_line(label, value, passes):
    """Return one consistently formatted rule result."""
    status = "pass" if passes else "FAIL"
    return f"{label}: {value:.1f} {status}"


def largest_single_company_weight(weights):
    """Combine all securities for each non-exempt company and return the largest."""
    company_weights = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0) + weight
    return max(company_weights.values(), default=0)


def check_candidate(name, weights, reserve_minimum):
    """Print all checkable rules and a verdict for one candidate."""
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weight for holding, weight in weights.items() if HOLDINGS[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding]["business_days_to_redeem"] <= LIQUIDITY_WINDOW
    )
    largest_company = largest_single_company_weight(weights)

    checks = [
        ("Weights sum to 100", total_weight, total_weight == 100),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight, reserve_weight >= reserve_minimum),
        (
            f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", largest_company, largest_company <= ISSUER_LIMIT),
    ]

    print(f"\nCandidate {name}")
    for label, value, passes in checks:
        print(result_line(label, value, passes))
    print("Calendar-year loss: requires CIO clarification")

    failed_checks = sum(not passes for _, _, passes in checks)
    if failed_checks == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failed_checks} rule(s)")


def main():
    reserve_minimum = (
        QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")

    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
