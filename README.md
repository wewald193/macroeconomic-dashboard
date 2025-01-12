# Macroeconomic Dashboard

A Python-based interactive dashboard for visualizing and analyzing key macroeconomic indicators using Streamlit. The dashboard combines data from Financial Modeling Prep (FMP) API with AI-powered insights to provide comprehensive economic analysis.

## Features

- **Time Series Visualization**: Interactive line charts with labeled axes and hover functionality
- **Key Statistics**: Display of recent, maximum, and minimum values for all indicators
- **Correlation Heatmap**: Visual representation of correlations between economic indicators
- **Side-by-Side Comparison**: Compare trends between any two indicators
- **AI-Generated Insights**:
  - Trend summaries powered by OpenAI
  - Context-aware Q&A functionality
- **Dynamic Filtering**: Customizable date ranges for tailored analysis

## Project Structure

```plaintext
macroeconomic-dashboard/
│
├── fetch_data.py            # Script to fetch raw macroeconomic data
├── clean_data.py           # Script to clean and preprocess fetched data
├── merge_cleaned_files.py  # Script to merge cleaned data for analysis
├── exploratory_analysis.py # Standalone script for exploratory data analysis
├── dashboard.py            # Streamlit app for visualization and AI insights
├── validate_data.py        # Script to validate raw data files
├── requirements.txt        # List of required libraries
├── data/                  # Folder containing raw data files
├── cleaned_data/         # Folder containing cleaned and processed data
└── .env                  # File for API keys (created by the user)
```

## Requirements

- Python 3.x
- Required Python libraries:
  - pandas
  - matplotlib
  - seaborn
  - openai
  - python-dotenv
  - streamlit
  - requests

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/macroeconomic-dashboard.git
   cd macroeconomic-dashboard
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **API Setup**

   To run the dashboard, you need to obtain API keys for the required services:

   **Financial Modeling Prep API Key**
   * Visit Financial Modeling Prep and sign up for an account.
   * Once logged in, navigate to the API section and generate your API key.

   **OpenAI API Key**
   * Visit OpenAI and create an account (if you don't already have one).
   * Go to the API Keys section in your account settings to generate a new API key.

   After obtaining your API keys, create a `.env` file in the root directory of the project and add the following:
   ```plaintext
   FMP_API_KEY=your_fmp_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```
   Replace `your_fmp_api_key` and `your_openai_api_key` with your actual API keys.

4. **Prepare the Data**
   ```bash
   # Fetch raw data
   python fetch_data.py

   # Clean the fetched data
   python clean_data.py

   # Merge cleaned data for analysis
   python merge_cleaned_files.py
   ```

5. **Launch the Dashboard**
   ```bash
   streamlit run dashboard.py
   ```

## Data Visualization

The dashboard includes visualizations for key macroeconomic indicators:
- Real GDP
- Inflation Rate
- Unemployment Rate
- Federal Funds Rate

## LLM Integration

- **Model**: Uses OpenAI's GPT-4 for generating insights and answering questions
- **Cost Consideration**: Implements efficient querying and filtering to optimize API usage costs

## Future Improvements

- Integration of additional economic indicators
- Expanded visualization options
- Docker containerization support
- Enhanced NLP capabilities for Q&A functionality

## Contributing

Feel free to open issues or submit pull requests to help improve the dashboard.
