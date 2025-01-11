import os
import pandas as pd

# Directory containing cleaned files
cleaned_data_dir = "cleaned_data/"
merged_file_path = "cleaned_data/merged_indicators.csv"

# List of cleaned files and their corresponding indicators
indicators = {
    "Real GDP": "cleaned_Real_GDP.csv",
    "Inflation Rate": "cleaned_Inflation_Rate.csv",
    "Unemployment Rate": "cleaned_Unemployment_Rate.csv",
    "Federal Funds Rate": "cleaned_Federal_Funds_Rate.csv",
}

def resample_to_monthly(df, date_column="date", method="ffill"):
    """
    Resample the DataFrame to monthly frequency.
    """
    # Convert the 'date' column to datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    df.set_index(date_column, inplace=True)

    # Drop duplicate dates
    if df.index.duplicated().any():
        print("Duplicate dates found. Dropping duplicates.")
        df = df[~df.index.duplicated(keep="first")]

    # Resample to monthly frequency
    if method == "ffill":
        df = df.resample("M").ffill()  # Forward-fill missing values
    elif method == "linear":
        df = df.resample("M").interpolate(method="linear")  # Linear interpolation
    else:
        raise ValueError(f"Unsupported resampling method: {method}")

    return df.reset_index()


def merge_cleaned_files(indicators, cleaned_data_dir, save_path):
    """
    Merge cleaned files into a single DataFrame with monthly frequency.
    """
    merged_df = None

    for indicator, filename in indicators.items():
        filepath = os.path.join(cleaned_data_dir, filename)
        if os.path.exists(filepath):
            print(f"Loading and resampling data for {indicator}...")
            df = pd.read_csv(filepath)

            # Rename 'value' column to the indicator name for clarity
            df.rename(columns={"value": indicator}, inplace=True)

            # Debug: Check for duplicate dates before resampling
            duplicate_dates = df["date"].duplicated().sum()
            if duplicate_dates > 0:
                print(f"Warning: {duplicate_dates} duplicate dates found in {indicator}. Fixing...")

            # Resample to monthly frequency
            df = resample_to_monthly(df, date_column="date", method="ffill")

            # Merge with the combined DataFrame
            if merged_df is None:
                merged_df = df  # Initialize with the first DataFrame
            else:
                merged_df = pd.merge(merged_df, df, on="date", how="outer")
        else:
            print(f"File not found: {filepath}")

    # Sort the merged DataFrame by date
    if merged_df is not None:
        merged_df.sort_values(by="date", inplace=True)
        merged_df.to_csv(save_path, index=False)
        print(f"Merged data saved to {save_path}")
    else:
        print("No files were merged.")


def main():
    merge_cleaned_files(indicators, cleaned_data_dir, merged_file_path)

if __name__ == "__main__":
    main()
