import os
import requests
import pandas as pd

# Load your API key from an environment variable
api_key = os.getenv("FMP_API_KEY")

# Define the single indicator you want to fetch
indicator_name = "Real GDP"
api_name = "realGDP"  # Correct 'name' parameter for the API call

# Build the API URL
url = f"https://financialmodelingprep.com/api/v4/economic?name={api_name}&apikey={api_key}"

# Fetch data from the API
response = requests.get(url)

# Process the response
if response.status_code == 200:
    print(f"API call successful for {indicator_name}")
    data = response.json()

    # Save the data to a CSV file if it's not empty
    if data:
        df = pd.DataFrame(data)
        filename = f"data/{indicator_name.replace(' ', '_')}.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print(f"No data returned for {indicator_name}.")
else:
    print(f"API call failed: {response.status_code} - {response.text}")
