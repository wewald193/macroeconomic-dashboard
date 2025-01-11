import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Use a valid seaborn style
plt.style.use("seaborn-v0_8-whitegrid")
sns.set(style="whitegrid")

# Load the merged dataset
merged_file_path = "cleaned_data/merged_indicators.csv"
data = pd.read_csv(merged_file_path)

# Convert the 'date' column to datetime format and set as index
data["date"] = pd.to_datetime(data["date"])
data.set_index("date", inplace=True)

# Normalize data for better visualization
def normalize_columns(df, columns):
    """
    Normalize selected columns to the range [0, 1] using min-max scaling.
    """
    df_normalized = df.copy()
    for col in columns:
        min_val = df[col].min()
        max_val = df[col].max()
        df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
    return df_normalized

# Plotting functions
def plot_line_chart(data, y_columns, title, normalize=False):
    """
    Plot a line chart comparing multiple indicators over time.
    Optionally normalize the indicators for better visualization.
    """
    if normalize:
        data = normalize_columns(data, y_columns)
        title += " (Normalized)"

    plt.figure(figsize=(12, 6))
    for column in y_columns:
        plt.plot(data.index, data[column], marker="o", markersize=3, label=column)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_scatter(data, x_column, y_column, title):
    """
    Plot a scatter plot to analyze correlation between two indicators.
    """
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=data[x_column], y=data[y_column], s=10)
    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)
    plt.show()

def plot_correlation_heatmap(df):
    """
    Compute the correlation matrix and display it as a heatmap.
    """
    # Compute the correlation matrix
    correlation_matrix = df.corr()

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap of Economic Indicators")
    plt.show()

# Main script
def main():
    # Line Chart: Trends over time for all indicators (normalized)
    print("Generating line chart for all indicators...")
    plot_line_chart(data, y_columns=data.columns, title="Economic Indicators Over Time", normalize=True)

    # Scatter Plot: Real GDP vs Federal Funds Rate
    if "Real GDP" in data.columns and "Federal Funds Rate" in data.columns:
        print("Generating scatter plot for Real GDP vs Federal Funds Rate...")
        plot_scatter(data, x_column="Real GDP", y_column="Federal Funds Rate", title="Real GDP vs Federal Funds Rate")

    # Scatter Plot: Inflation Rate vs Unemployment Rate
    if "Inflation Rate" in data.columns and "Unemployment Rate" in data.columns:
        print("Generating scatter plot for Inflation Rate vs Unemployment Rate...")
        plot_scatter(data, x_column="Inflation Rate", y_column="Unemployment Rate", title="Inflation Rate vs Unemployment Rate")

    # Correlation Heatmap
    print("Generating correlation heatmap...")
    numeric_columns = data.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_columns) > 1:
        plot_correlation_heatmap(data[numeric_columns])
    else:
        print("Not enough numeric columns to compute correlations.")

# Insights from the Correlation Heatmap:
# 1. **Real GDP vs Federal Funds Rate** (-0.42):
#    - A moderate negative correlation aligns with the IS-LM model.
#    - Higher interest rates (tight monetary policy) reduce investment and GDP.
#
# 2. **Inflation Rate vs Federal Funds Rate** (0.36):
#    - Positive correlation reflects monetary policy's response to inflation.
#    - Central banks raise rates to counter high inflation, as per the Taylor Rule.
#
# 3. **Unemployment Rate vs Inflation Rate** (-0.20):
#    - Weak negative correlation aligns with the Phillips Curve.
#    - Inflation and unemployment show an inverse relationship, though weak.
#
# 4. **Real GDP vs Unemployment Rate** (0.06):
#    - Weak correlation challenges Okun's Law, suggesting atypical economic conditions.
#    - Lag effects or structural factors may obscure the expected inverse relationship.
#
# 5. **Real GDP vs Inflation Rate** (-0.03):
#    - Minimal correlation indicates a decoupling of growth and inflation.
#    - Could reflect a period of stagflation or stable prices during growth.
#
# 6. **Unemployment Rate vs Federal Funds Rate** (0.06):
#    - Little correlation suggests unemployment reacts to more than just monetary policy.
#    - Structural unemployment or time lags might explain the weak relationship.


if __name__ == "__main__":
    main()
