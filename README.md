# Macroeconomic Dashboard

This project visualizes key macroeconomic indicators using Python and Streamlit. The dashboard includes:
- Data fetching from the Financial Modeling Prep (FMP) API.
- Interactive visualizations of economic data (e.g., GDP, inflation, unemployment).
- LLM-powered summaries and Q&A functionality using OpenAI.

## Requirements
- Python 3.x
- Libraries: `requests`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `streamlit`, `openai`

## Project Structure
- `fetch_data.py`: Script to fetch data from the API.
- `dashboard.py`: Streamlit app for data visualization.
- `data/`: Folder for raw and cleaned data.

## How to Run
1. Activate the virtual environment.
2. Run the dashboard:
   ```bash
   streamlit run dashboard.py
