import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multitest import multipletests


def test_primary_metric(df: pd.DataFrame , alpha = 0.05):
    """
    Primary Metric Analysis (Conversion Rate) via Two-Proportion Z-test
    """
    # Validating that the Dataset is Pandas DataFrame
    if not isinstance(df , pd.DataFrame):
        raise TypeError("The Dataset Must be Pandas DataFrame")

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")

    if df[["variant", "converted"]].isna().any().any():
        raise ValueError("Missing values in metric columns.")


    if not df["converted"].isin([0, 1]).all():
        raise ValueError("converted must contain only 0 and 1.")



    summary = df.groupby("variant").agg(
        total_conversions = ('converted' , 'sum'),
        total_users = ('converted' , 'count'),
        conversion_rate = ('converted' , 'mean')
    )

    if not {"control", "treatment"}.issubset(summary.index):
        raise ValueError("Both experiment groups must be present.")

    # Extract Control & Treatment stats
    treatment = summary.loc['treatment']
    control = summary.loc['control']

    p_C = float(control["conversion_rate"])
    p_T = float(treatment["conversion_rate"])
    n_C = int(control["total_users"])
    n_T = int(treatment["total_users"])

    # Performing the TWo-Proportion Z-test
    count = [treatment["total_conversions"] , control["total_conversions"]]
    observations = [n_T , n_C]

    z_stat , p_value = proportions_ztest(count= count , nobs= observations , alternative= 'two-sided')

    # Absoulte and Relative lift & CI
    abs_lift = p_T - p_C
    relative_lift = (abs_lift / p_C) * 100

    # Calculating the Standard Error difference and Confidence Interval
    se_diff = np.sqrt(((p_T * (1-p_T)) /n_T) + ((p_C * (1-p_C)) / n_C))
    z_crit = stats.norm.ppf(1 - (alpha/2))
    margin_of_error = z_crit * se_diff

    ci_lower_rel = ((abs_lift - margin_of_error) / p_C) * 100
    ci_upper_rel = ((abs_lift + margin_of_error) / p_C) * 100

    print("=" * 60)
    print("PRIMARY METRIC CONVERISON RATE (TWO-PROPORTION Z-TEST)")
    print("=" * 60)
    print(f"Treatment Conversion Rate: {p_T:.4%}")
    print(f"Control Conversion Rate: {p_C:.4%}")
    print(f"Relative Lift Between the Treatment and Control Group: {relative_lift:+.2f}%")
    print(f"{(1-alpha)*100:.0f}% CI for Lift:    [{ci_lower_rel:+.2f}%, {ci_upper_rel:+.2f}%]")
    print(f"Z-Statistic: {z_stat:.4f} | p-value: {p_value}")

    if p_value < alpha:
        print(f"Reject H0: Redesign changed conversion rate. Statistically Significant (p < {alpha}).")
    else:
        print(f"Fail to reject H0. There is No Significant Difference Between the Old and the New Conversion Rates (p >= {alpha}).")

    return {
        "p_value": p_value,
        "rel_lift": relative_lift,
        "ci_rel": (ci_lower_rel, ci_upper_rel)
        }



def test_secondary_metric(df: pd.DataFrame , alpha = 0.05):
    """
    Secondary Metric Analysis: Average Order Value  (AOV) via Welch t-Test
    """
    # Ensuring that the Dataset is a Pandas DataFrame
    if not isinstance(df , pd.DataFrame):
        raise TypeError("The Dataset Must be a Pandas DataFrame")

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")

    if df[["variant", "converted" , "user_revenue" , "order_count"]].isna().any().any():
            raise ValueError("Missing values in metric columns.")


    # Filter for converted users only (AOV applies only to purchases)
    converting_df = df[df["converted"] == 1].copy()
    converting_df["user_aov"] = (converting_df["user_revenue"] / converting_df["order_count"])

    # Defining the Treatment And Control Group
    treatment_aov = converting_df[converting_df["variant"] == 'treatment']["user_aov"]
    control_aov = converting_df[converting_df["variant"] == 'control']["user_aov"]

    # Summary of Some Statistics
    mean_T = treatment_aov.mean()
    mean_C = control_aov.mean()
    n_T = len(treatment_aov)
    n_C = len(control_aov)

    # =========================================================================
    # Hypothesis Testing Assumptions
    # =========================================================================
    # H0: The Redesign Has No Effect On The Average Order Value (mean_T = mean_C)
    # H1: The Redesign Significantly Changes The Average Order Value (mean_T != mean_C)
    # Test Selection: Welch's t-test (two-sided)
    # Reason: Continuous monetary metric with unequal group variances (equal_var=False)



    # Perfoming Welch t-test
    t_stat , p_value = stats.ttest_ind(a= treatment_aov ,b= control_aov , equal_var= False)
    # Absolute Relative Lift and Confidence Interval
    abs_lift = mean_T - mean_C
    
    relative_lift = (abs_lift / mean_C) * 100
    se_diff = np.sqrt((treatment_aov.var(ddof=1) / n_T) + (control_aov.var(ddof=1) / n_C))
    t_crit = stats.t.ppf(1 - (alpha / 2))
    margin_of_error = se_diff * t_crit

    # Computing the Confidence Interval
    ci_lower_rel = ((abs_lift - margin_of_error) / mean_C) * 100
    ci_upper_rel = ((abs_lift + margin_of_error) / mean_C) * 100

    print("=" * 60)
    print("SECONDARY METRIC: AVERAGE ORDER VALUE (WELCH'S T-TEST)")
    print("=" * 60)
    print(f"Treatment AOV: ${mean_T:.2f}")
    print(f"Control AOV: ${mean_C:.2f}")
    print(f"Relative Lift: {relative_lift:+.2f}%")
    print(f"{(1-alpha)*100:.0f}% CI for Lift: [{ci_lower_rel:+.2f}%, {ci_upper_rel:+.2f}%]")
    print(f"t-Statistic: {t_stat:.4f} | p-value: {p_value}")

    # Decision Rule
    if p_value < alpha:
        print(f"Reject H0: Redesign changed Average Order Value (p < {alpha}).")
    else:
        print(f"Fail to reject H0: No significant difference in AOV (p >= {alpha}).")

    return {
        "p_value": p_value,
        "rel_lift": relative_lift,
        "ci_rel": (ci_lower_rel, ci_upper_rel),
    }

