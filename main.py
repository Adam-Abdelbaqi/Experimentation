from src.data import load_data
from src.hypothesis_testing import test_primary_metric, test_secondary_metric
from src.power_analysis import power_analysis
from src.srm_check import run_srm_check


ALPHA = 0.05
EXPECTED_RATIO = (0.5, 0.5)


def main():
    """Run the checkout redesign A/B test analysis."""

    print("=" * 60)
    print("CHECKOUT REDESIGN A/B TEST")
    print("=" * 60)

    # Loading and Cleaning the Dataset
    df = load_data(r"C:\Users\Dell\Desktop\Adam\Experiments\Etsy-checkout-abtest\data\processed\Redesign_checkout.csv")


    print(f"Dataset loaded successfully: {len(df):,} users")
    print("Experiment allocation:\n"
        f"{df['variant'].value_counts().to_string()}")

    # Sample Ratio Mismatch (SRM)
    print("\n[2] SAMPLE RATIO MISMATCH (SRM)")
    print("-" * 65)
    print(
        "Objective: Check whether the observed allocation between "
        "control and treatment is consistent with the expected "
        "50/50 experiment design.")
    print(
        f"Significance level: {ALPHA:.0%}\n"
        "H0: Observed allocation matches the expected ratio.\n"
        "H1: Observed allocation differs from the expected ratio.")
   
    
    srm_p_value = run_srm_check(
        df,
        expected_ratio= EXPECTED_RATIO,
        alpha= ALPHA
    )

    srm_detected = srm_p_value < ALPHA


    # Primary metric: conversion rate
    print("\n[3] PRIMARY METRIC — CONVERSION RATE")
    print("-" * 65)
    print(
        "Objective: Determine whether the checkout redesign changes "
        "the proportion of users who complete a purchase.\n"
        "Test: Two-proportion z-test, two-sided.\n"
        "H0: Treatment and control conversion rates are equal.\n"
        "H1: Treatment and control conversion rates differ.")
    
    primary_metric_result = test_primary_metric(df, alpha= ALPHA)

    # Secondary metric: average order value
    print("\n[4] SECONDARY METRIC — AVERAGE ORDER VALUE (AOV)")
    print("-" * 65)
    print(
        "Objective: Compare average revenue per order among users "
        "who completed a purchase.\n"
        "Test: Welch's independent-samples t-test, two-sided.\n"
        "H0: Mean user-level AOV is equal across the two groups.\n"
        "H1: Mean user-level AOV differs between the two groups.")

    
    secondary_metric_result = test_secondary_metric(
        df,
        alpha=ALPHA,)

    

      # 5. Final summary
    print("\n" + "=" * 65)
    print("FINAL RESULTS SUMMARY")
    print("=" * 65)

    print("\nDATA INTEGRITY")
    print(f"SRM p-value: {srm_p_value:.6g}")

    if srm_detected:
        print(
            "Result: SRM detected. Investigate the allocation "
            "and data collection process before drawing conclusions."
        )
    else:
        print(
            "Result: No statistically significant SRM detected. "
            "This does not prove that allocation was error-free."
        )

    print("\nPRIMARY METRIC: CONVERSION RATE")
    print(
        f"Relative lift: "
        f"{primary_metric_result['rel_lift']:+.2f}%")
    
    print(
        f"95% confidence interval for relative lift: "
        f"{primary_metric_result['ci_rel']}")
    print(
        f"p-value: {primary_metric_result['p_value']:.6g}")

    if primary_metric_result["p_value"] < ALPHA:
        print(
            "Conclusion: Reject H0. The observed conversion-rate "
            "difference is statistically significant at the "
            f"{ALPHA:.0%} level.")
    else:
        print(
            "Conclusion: Fail to reject H0. The data do not provide "
            "sufficient evidence of a conversion-rate difference "
            f"at the {ALPHA:.0%} level.")

    print("\nSECONDARY METRIC: AVERAGE ORDER VALUE")
    print(
        f"Relative lift: "
        f"{secondary_metric_result['rel_lift']:+.2f}%")
   
    print(
        f"95% confidence interval for relative lift: "
        f"{secondary_metric_result['ci_rel']}")
    print(
        f"p-value: {secondary_metric_result['p_value']:.6g}")

    if secondary_metric_result["p_value"] < ALPHA:
        print(
            "Conclusion: Reject H0. Mean user-level AOV differs "
            "significantly between the observed groups.")
    else:
        print(
            "Conclusion: Fail to reject H0. The data do not provide "
            "sufficient evidence of a difference in mean user-level "
            "AOV at the specified significance level.")

if __name__ == "__main__":
    main()
