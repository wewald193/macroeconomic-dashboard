import os
import pandas as pd

# Directory paths
raw_data_dir = "data/"
cleaned_data_dir = "cleaned_data/"
os.makedirs(cleaned_data_dir, exist_ok=True)

# List of indicators and their file paths
indicators = {
    "Real GDP": "Real_GDP.csv",
    "Inflation Rate": "Inflation_Rate.csv",
    "Unemployment Rate": "Unemployment_Rate.csv",
    "Federal Funds Rate": "Federal_Funds_Rate.csv",
}

def clean_csv(filepath, save_path):
    """
    Clean the given CSV file and save the cleaned version.
    """
    print(f"Cleaning file: {filepath}...")

    try:
        # Load the raw data
        df = pd.read_csv(filepath)

        # Convert 'date' column to datetime format
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        else:
            raise ValueError("Missing 'date' column in file.")

        # Rename columns to standard format
        df.rename(columns={"date": "date", "value": "value"}, inplace=True)

        # Handle missing values (drop rows with missing data)
        df.dropna(inplace=True)

        # Sort by date
        df.sort_values(by="date", inplace=True)

        # Save the cleaned data
        df.to_csv(save_path, index=False)
        print(f"Cleaned data saved to {save_path}")
    except Exception as e:
        print(f"Error cleaning file {filepath}: {e}")

def main():
    for indicator, filename in indicators.items():
        raw_filepath = os.path.join(raw_data_dir, filename)
        cleaned_filepath = os.path.join(cleaned_data_dir, f"cleaned_{filename}")

        if os.path.exists(raw_filepath):
            clean_csv(raw_filepath, cleaned_filepath)
        else:
            print(f"File not found: {raw_filepath}")

if __name__ == "__main__":
    main()
