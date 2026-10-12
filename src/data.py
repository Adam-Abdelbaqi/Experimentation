import pandas as pd


def load_data(filepath)-> pd.DataFrame:
    """
    Loads Redesign Checkout Dataset
    """
    
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Dataset File is not found {filepath}") from e

    # Ensuring that the Dataset is not empty
    if df.empty:
        raise ValueError(f"The Dataset at {filepath} is Empty")


    required_cols = {'user_id' , 'variant' , 'device' , 'visitor_type' , 'converted' , 'user_revenue' , 'order_count'}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:        
        raise ValueError(f"Missing required columns in dataset: {missing_cols}")

    # Ensure that the Dataset are free from Duplicates
    if not df['user_id'].is_unique:
        raise ValueError(f"Duplicate User_IDs found in dataset.")

    # Ensure that there is no missing values
    if df.isna().any().any():
        raise ValueError("The dataset contains missing (NaN) values.")


    # 6. Value Domain Validation
    if not df["converted"].isin([0, 1]).all():
        raise ValueError("'converted' column must only contain 0 or 1.")

    if (df["user_revenue"] < 0).any():
        raise ValueError("'user_revenue' cannot contain negative values.")

    return df
    


    