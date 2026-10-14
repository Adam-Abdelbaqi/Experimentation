# Etsy Checkout Redesign — A/B Testing Analysis

## Project Overview

This project evaluates a hypothetical Etsy checkout redesign using an educational, simulated dataset. The objective is to determine whether the redesigned checkout experience improves user conversion without relying on intuition alone.

The project follows a structured experimentation workflow, covering experiment assumptions, sample size planning, Sample Ratio Mismatch (SRM) checks, hypothesis testing, and visualization of experiment results.

**Note:** This is an educational project. The dataset is simulated, and the experiment does not represent an actual Etsy experiment.

## Objectives

- Evaluate whether the redesigned checkout improves conversion rate.
- Check whether the observed treatment allocation is consistent with the expected assignment ratio.
- Apply statistical hypothesis testing and interpret p-values.
- Conduct pre-experiment power analysis and sample size planning.
- Examine average order value (AOV) as a secondary metric.
- Communicate statistical findings through visualizations and practical interpretations.

## Dataset

The dataset contains user-level observations with the following columns:

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `variant` | Experiment group assignment |
| `device` | User's device category |
| `visitor_type` | Visitor classification |
| `converted` | Whether the user converted |
| `user_revenue` | Revenue attributed to the user |
| `order_count` | Number of orders attributed to the user |

The analysis assumes a **50/50 allocation** between the control and treatment groups because the original assignment ratio is not specified.

## Experiment Design

- **Control group:** Existing checkout experience.
- **Treatment group:** Hypothetical redesigned checkout experience.
- **Expected allocation:** 50% control and 50% treatment.
- **Significance level:** (alpha = 0.05).
- **Primary metric:** Conversion rate.
- **Secondary metric:** Average order value among converting users.

These are educational assumptions rather than verified details of an actual Etsy experiment.

## Methodology

### 1. Pre-experiment planning

Power analysis is used to determine the sample size required to detect a meaningful difference between the groups. The analysis uses a specified significance level, statistical power, and minimum detectable effect (MDE).

### 2. Sample Ratio Mismatch (SRM)

The observed allocation between control and treatment is compared with the expected 50/50 allocation using a chi-square goodness-of-fit test.

An SRM check helps identify unexpected assignment imbalances that may indicate problems with experiment implementation or data collection.

### 3. Primary metric: Conversion rate

A two-proportion z-test compares conversion rates between the control and treatment groups.

- **Null hypothesis ((H_0)):** The population conversion rates are equal.
- **Alternative hypothesis ((H_1)):** The population conversion rates differ.

The significance level is set to 0.05. The analysis considers the estimated difference in conversion rates alongside statistical significance.

### 4. Secondary metric: Average order value

Welch's two-sample t-test compares average order value among converting users, without assuming equal population variances.

This metric is interpreted cautiously because conditioning on conversion can introduce post-treatment selection effects. AOV among converters alone does not necessarily measure the overall causal effect on revenue.

### 5. Visualization and interpretation

Visualizations are used to explore the experiment data, compare group-level metrics, and communicate the findings. Statistical results are interpreted in both technical and practical terms.

## Project Structure

The repository is organized around the analysis notebook, reusable Python scripts, SQL preparation, and project documentation. The exact filenames may vary.

```text
Etsy-checkout-abtest/
├── data/
│   ├── processed/
│   └── raw/
├── notebooks/
│   └── full_experiment_analysis.ipynb
├── sql/
│   └── Checkout_Redesign.sql
├── src/
│   ├── __pycache__/
│   ├── data.py
│   ├── hypothesis_testing.py
│   ├── power_analysis.py
│   ├── segment_analysis.py
│   └── srm_check.py
├── __init__.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt

```

## Installation and Usage

### Prerequisites

- Python 3.14 or a compatible version for the installed dependencies.
- Git.
- The project dataset in the expected location.

### 1. Clone the repository

```bash
git clone https://github.com/Adam-Abdelbaqi/Experimentation.git
cd Experimentation
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the analysis

Run the analysis script from the directory containing it, using the appropriate path for your repository:

```bash
python src/main.py
```

Open the Jupyter notebook in VS Code to explore the analysis, visualizations, and pre-experiment planning.

**Note:** Update the execution command and project structure above if your files are located directly in the repository root or use different filenames.

## Results

Record the actual output of the analysis here before publishing the final README:

- **Control conversion rate:** To be filled from analysis output.
- **Treatment conversion rate:** To be filled from analysis output.
- **Absolute conversion-rate difference:** To be filled from analysis output.
- **Conversion-rate hypothesis test:** Report the p-value and conclusion.
- **SRM check:** Report the result of the allocation check.
- **AOV comparison:** Report the estimated difference, p-value, and limitations.

Statistical significance should not be interpreted as proof of business impact. The magnitude of the estimated effect and its uncertainty should also inform the decision.

## Limitations

- The dataset is simulated and may not reflect real Etsy users or purchasing behavior.
- The 50/50 assignment ratio is an explicit assumption.
- The analysis depends on the validity of the experiment design and the available data.
- The secondary AOV analysis is restricted to converters and may be affected by post-treatment selection.
- Statistical significance alone does not establish practical or commercial significance.

## Skills Demonstrated

- Statistical hypothesis testing
- A/B testing and experimental design
- Power analysis and sample size estimation
- Sample Ratio Mismatch detection
- Conversion-rate analysis
- Welch's t-test
- Python, pandas, NumPy, SciPy, and statistical analysis
- Data visualization and communicating experimental results
- SQL-based data preparation
