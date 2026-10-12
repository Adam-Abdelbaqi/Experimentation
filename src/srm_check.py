import pandas as pd
from scipy import stats
from src.data import load_data

def run_srm_check(df: pd.DataFrame , expected_ratio = (0.5 , 0.5) , alpha = 0.05):
    """
    Chi-Square Goodness-of-Fit test for Sample Ratio Mismatch
    """
    # Ensuring that the dataset is a dataframe
    if not isinstance(df , pd.DataFrame):
        raise TypeError("The Dataset must be a DataFrame")

    observed = df['variant'].value_counts().sort_index()
    total_users = observed.sum()
    expected = [total_users * r for r in expected_ratio]

    # Performing the Chi-Square Test
    chi2 , p_value = stats.chisquare(f_obs= observed , f_exp= expected)

    expected_dict = {
    var: round(exp) for var, exp in zip(observed.index, expected)
    }

    print("=" * 60)
    print("SAMPLE RATIO MISMATCH (SRM) CHECK")
    print("=" * 60)
    print(f"Observed Counts: {observed.to_dict()}")
    print(f"Expected Counts: {expected_dict}")
    print(f"Chi-Square Stat: {chi2:.4f} | p-value: {p_value:.4f}")

    # Assuming that our significance level (alpha) = 0.05
    # Test Assumptions:
    # H0: The observed traffic distribution matches the expected design distribution (e.g., exactly 50% Control, 50% Treatment) (NO SRM)
    # H1:  The observed traffic distribution does not match the expected design distribution (SRM Present)
    if p_value > alpha:
        print(f"Failed to Reject H0. No SRM Detected (split matches 50/50).")
    else:
        print(f"Reject H0. The observed traffic distribution deviate significantly from the expected distribuiton (SRM Detected).")

    return p_value


mydf = load_data(r"C:\Users\Dell\Desktop\Adam\Experiments\Etsy-checkout-abtest\data\processed\Redesign_checkout.csv")
results = run_srm_check(mydf)
