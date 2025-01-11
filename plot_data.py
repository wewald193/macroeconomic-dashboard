import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing the CSV files
data_dir = "data/"
indicators = {
    "Real GDP (Gross Domestic Product)": "Real_GDP.csv",
    "Inflation Rate": "Inflation_Rate.csv",
    "Unemployment Rate": "Unemployment_Rate.csv",
    "Federal Funds Rate": "Federal_Funds_Rate.csv",
}

def plot_time_series(filepath, title):
    """
    Plot a time series for the given file.
    """
    try:
        # Load the data
        df = pd.read_csv(filepath)

        # Convert 'date' column to datetime
        df["date"] = pd.to_datetime(df["date"])

        # Plot the time series with smaller markers
        plt.figure(figsize=(10, 6))
        plt.plot(df["date"], df["value"], marker="o", markersize=4, linestyle="-", label=title)
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Error plotting {title}: {e}")

def main():
    for indicator, filename in indicators.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            print(f"Plotting {indicator}...")
            plot_time_series(filepath, f"{indicator} Over Time")
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
