import os
import pandas as pd

# Directory containing CSV files
data_dir = "data/"
indicators = {
    "Real GDP": "Real_GDP.csv",
    "Inflation Rate": "Inflation_Rate.csv",
    "Unemployment Rate": "Unemployment_Rate.csv",
    "Federal Funds Rate": "Federal_Funds_Rate.csv",
}

def validate_csv(filepath):
    """
    Validate a CSV file by checking for missing values and proper formatting of the date column.
    """
    print(f"Validating file: {filepath}...")
    try:
        # Load the data
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Check for missing values
    missing_values = df.isnull().sum()
    print("Missing values:")
    print(missing_values)

    # Ensure 'date' column exists and is properly formatted
    if "date" in df.columns:
        try:
            df["date"] = pd.to_datetime(df["date"])
            print("Date column is present and properly formatted.")
        except Exception as e:
            print(f"Error in date column formatting: {e}")
    else:
        print("Date column is missing!")

    print("-" * 50)

def main():
    for indicator, filename in indicators.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            validate_csv(filepath)
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
