import os
import requests
import pandas as pd

# Fetch functions for each indicator
def fetch_real_gdp(api_key):
    """
    Fetch Real GDP data from the FMP API.
    """
    url = f"https://financialmodelingprep.com/api/v4/economic?name=realGDP&apikey={api_key}"
    response = requests.get(url)
    return response.json()

def fetch_inflation_rate(api_key):
    """
    Fetch Inflation Rate data from the FMP API.
    """
    url = f"https://financialmodelingprep.com/api/v4/economic?name=inflationRate&apikey={api_key}"
    response = requests.get(url)
    return response.json()

def fetch_unemployment(api_key):
    """
    Fetch Unemployment Rate data from the FMP API.
    """
    url = f"https://financialmodelingprep.com/api/v4/economic?name=unemploymentRate&apikey={api_key}"
    response = requests.get(url)
    return response.json()

def fetch_federal_funds(api_key):
    """
    Fetch Federal Funds Rate data from the FMP API.
    """
    url = f"https://financialmodelingprep.com/api/v4/economic?name=federalFunds&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Save function
def save_as_csv(data, filename):
    """
    Convert JSON data to a Pandas DataFrame and save it as a CSV file.
    """
    if data:  # Only save if data is not empty
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print(f"No data available for {filename}. File not created.")

# Main script
def main():
    # Load API key
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: API key not found. Please set your FMP_API_KEY environment variable.")
        return

    # Create a directory for the data
    data_dir = "data/"
    os.makedirs(data_dir, exist_ok=True)

    # Fetch and save Real GDP data
    print("Fetching Real GDP data...")
    gdp_data = fetch_real_gdp(api_key)
    save_as_csv(gdp_data, f"{data_dir}Real_GDP.csv")

    # Fetch and save Inflation Rate data
    print("Fetching Inflation Rate data...")
    inflation_data = fetch_inflation_rate(api_key)
    save_as_csv(inflation_data, f"{data_dir}Inflation_Rate.csv")

    # Fetch and save Unemployment Rate data
    print("Fetching Unemployment Rate data...")
    unemployment_data = fetch_unemployment(api_key)
    save_as_csv(unemployment_data, f"{data_dir}Unemployment_Rate.csv")

    # Fetch and save Federal Funds Rate data
    print("Fetching Federal Funds Rate data...")
    federal_funds_data = fetch_federal_funds(api_key)
    save_as_csv(federal_funds_data, f"{data_dir}Federal_Funds_Rate.csv")

    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    main()
