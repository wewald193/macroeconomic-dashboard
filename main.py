import os
from fetch_data import (
    fetch_real_gdp,
    fetch_inflation_rate,
    fetch_unemployment,
    fetch_federal_funds,
    save_as_csv,
)

def main():
    """
    Main script to fetch and save data for selected macroeconomic indicators.
    """
    # Load API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: API key not found. Please set your FMP_API_KEY environment variable.")
        return

    # Create a directory for saving the data
    data_dir = "data/"
    os.makedirs(data_dir, exist_ok=True)

    # Fetch and save data for each indicator
    print("Fetching Real GDP data...")
    gdp_data = fetch_real_gdp(api_key)
    save_as_csv(gdp_data, f"{data_dir}Real_GDP.csv")

    print("Fetching Inflation Rate data...")
    inflation_data = fetch_inflation_rate(api_key)
    save_as_csv(inflation_data, f"{data_dir}Inflation_Rate.csv")

    print("Fetching Unemployment Rate data...")
    unemployment_data = fetch_unemployment(api_key)
    save_as_csv(unemployment_data, f"{data_dir}Unemployment_Rate.csv")

    print("Fetching Federal Funds Rate data...")
    federal_funds_data = fetch_federal_funds(api_key)
    save_as_csv(federal_funds_data, f"{data_dir}Federal_Funds_Rate.csv")

    print("\nData fetching and saving completed successfully!")

if __name__ == "__main__":
    main()
