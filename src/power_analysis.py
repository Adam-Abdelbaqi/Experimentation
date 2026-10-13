import numpy as np
import statsmodels.stats.power as smp
from statsmodels.stats.proportion import proportion_effectsize


def power_analysis(p_C: float, n_per_group: int, alpha: float = 0.05, power: float = 0.80,):
    
    """
    PRE-EXPERIMENT PLANNING: Determines the Minimum Detectable Effect (MDE)
    given a fixed traffic/sample size budget.
   
    """

    power_calc = smp.NormalIndPower()

    # Calculate MDE effect size given available sample size
    mde_effect_size = power_calc.solve_power(nobs1= n_per_group, power= power, alpha= alpha, ratio=1.0)

    # Convert Cohen's h back to absolute & relative rates
    p_mde = np.sin(mde_effect_size / 2 + np.arcsin(np.sqrt(p_C))) ** 2
    abs_mde = p_mde - p_C
    rel_mde = (abs_mde / p_C) * 100

    print("=" * 60)
    print("PRE-EXPERIMENT POWER ANALYSIS (SAMPLE SIZE & MDE PLANNING)")
    print("=" * 60)
    print(f"Baseline Conversion Rate (p_C): {p_C:.4%} ({n_per_group:,} users/group)")
    print(f"Target Significance Level (alpha):   {alpha:.2f}")
    print(f"Target Statistical Power (1-beta): {power:.0%}")
    print(f"Minimum Detectable Effect (MDE): {rel_mde:+.2f}% relative ({abs_mde:+.2f}% absolute)")
    print(f"Target Conversion Rate needed:   {p_mde:.4%}")
    print("=" * 60)

    return rel_mde


