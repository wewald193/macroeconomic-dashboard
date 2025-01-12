import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import date
from openai import OpenAI
import altair as alt


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Title of the dashboard
st.title("Macroeconomic Dashboard")
st.markdown("### Explore trends and relationships among key economic indicators.")

# Directory containing cleaned data
data_dir = "cleaned_data/"

# List of indicators and their corresponding file names
indicators = {
    "Real GDP": "cleaned_Real_GDP.csv",
    "Inflation Rate": "cleaned_Inflation_Rate.csv",
    "Unemployment Rate": "cleaned_Unemployment_Rate.csv",
    "Federal Funds Rate": "cleaned_Federal_Funds_Rate.csv"
}

# Sidebar: Date range slider
st.sidebar.header("Filter Date Range")
min_date, max_date = pd.to_datetime("1947-01"), pd.to_datetime("2024-07")
start_date, end_date = st.sidebar.slider(
    "Select Date Range:",
    min_value=min_date.date(),
    max_value=max_date.date(),
    value=(min_date.date(), max_date.date()),
    format="YYYY-MM"
)

# Tabs for better organization
tab1, tab2, tab3, tab4 = st.tabs(["📈 Time Series Visualization", "📊 Key Statistics", "📉 Additional Visualizations", "💡 AI-Generated Insights"])

# Tab 1: Time Series Visualization
with tab1:
    st.subheader("Time Series Visualization")
    selected_indicator = st.selectbox("Choose an indicator to display:", list(indicators.keys()))
    if selected_indicator:
        file_path = os.path.join(data_dir, indicators[selected_indicator])

        if os.path.exists(file_path):
            # Load the data
            data = pd.read_csv(file_path, parse_dates=["date"])
            data.set_index("date", inplace=True)

            # Filter data based on the selected date range
            filtered_data = data.loc[start_date:end_date]

            # Check if filtered data is empty
            if filtered_data.empty:
                st.warning(f"No data available for {selected_indicator} in the selected date range ({start_date} to {end_date}).")
            else:
                # Display the filtered data as a line chart
                st.write(f"### {selected_indicator} Over Time")
                st.line_chart(filtered_data["value"], use_container_width=True)
        else:
            st.error(f"Data file not found for {selected_indicator}: {file_path}")


# Tab 2: Key Statistics
with tab2:
    st.subheader("Key Statistics and Comparison")

    # Individual statistics for each indicator
    for name, filename in indicators.items():
        file_path = os.path.join(data_dir, filename)
        st.markdown(f"#### {name}")
        if os.path.exists(file_path):
            data = pd.read_csv(file_path, parse_dates=["date"])
            data.set_index("date", inplace=True)

            # Filter data for the selected range
            filtered_data = data.loc[start_date:end_date]

            if not filtered_data.empty:
                most_recent_date = filtered_data.index[-1]
                most_recent_value = filtered_data["value"].iloc[-1]
                max_value = filtered_data["value"].max()
                max_date = filtered_data["value"].idxmax()
                min_value = filtered_data["value"].min()
                min_date = filtered_data["value"].idxmin()

                # Display stats
                st.write(f"**Most Recent Value ({most_recent_date.date()}):** {most_recent_value:.2f}")
                st.write(f"**Max Value ({max_date.date()}):** {max_value:.2f}")
                st.write(f"**Min Value ({min_date.date()}):** {min_value:.2f}")
            else:
                st.write("No data available for the selected range.")
        else:
            st.error(f"Data file not found for {name}.")


# Tab 3: Additional Visualizations
with tab3:
    st.subheader("Additional Visualizations")

    # Correlation Heatmap
    st.subheader("Correlation Heatmap of Economic Indicators")
    merged_file_path = os.path.join(data_dir, "merged_indicators.csv")
    if os.path.exists(merged_file_path):
        merged_data = pd.read_csv(merged_file_path, parse_dates=["date"])
        filtered_merged_data = merged_data[
            (merged_data["date"] >= pd.to_datetime(start_date)) & (merged_data["date"] <= pd.to_datetime(end_date))
        ]
        corr_matrix = filtered_merged_data.corr()

        # Plot heatmap using Seaborn
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
        st.pyplot(plt.gcf())
    else:
        st.error("Merged indicators file not found.")

    # Side-by-side comparison of two indicators
    st.subheader("Side-by-Side Comparison")
    indicator_1 = st.selectbox("Select the first indicator:", list(indicators.keys()), index=0, key="indicator_1")
    indicator_2 = st.selectbox("Select the second indicator:", list(indicators.keys()), index=1, key="indicator_2")

    # Option to normalize data
    normalize_data = st.checkbox("Normalize Data", value=False, key="normalize_data")

    if indicator_1 != indicator_2:
        file_path_1 = os.path.join(data_dir, indicators[indicator_1])
        file_path_2 = os.path.join(data_dir, indicators[indicator_2])

        if os.path.exists(file_path_1) and os.path.exists(file_path_2):
            data_1 = pd.read_csv(file_path_1, parse_dates=["date"])
            data_2 = pd.read_csv(file_path_2, parse_dates=["date"])

            # Filter data for the selected date range
            filtered_data_1 = data_1[
                (data_1["date"] >= str(start_date)) & (data_1["date"] <= str(end_date))
            ]
            filtered_data_2 = data_2[
                (data_2["date"] >= str(start_date)) & (data_2["date"] <= str(end_date))
            ]

            # Check if filtered data is empty for either indicator
            if filtered_data_1.empty and filtered_data_2.empty:
                st.warning(
                    f"No data available for both {indicator_1} and {indicator_2} in the selected date range ({start_date} to {end_date})."
                )
            elif filtered_data_1.empty:
                st.warning(f"No data available for {indicator_1} in the selected date range ({start_date} to {end_date}).")
            elif filtered_data_2.empty:
                st.warning(f"No data available for {indicator_2} in the selected date range ({start_date} to {end_date}).")
            else:
                # Merge the two filtered dataframes on the date column
                merged_comparison = pd.merge(
                    filtered_data_1, filtered_data_2, on="date", suffixes=(f" ({indicator_1})", f" ({indicator_2})")
                )

                # Normalize data if the checkbox is selected
                if normalize_data:
                    merged_comparison[f"value ({indicator_1})"] = (
                        merged_comparison[f"value ({indicator_1})"] - merged_comparison[f"value ({indicator_1})"].mean()
                    ) / merged_comparison[f"value ({indicator_1})"].std()
                    merged_comparison[f"value ({indicator_2})"] = (
                        merged_comparison[f"value ({indicator_2})"] - merged_comparison[f"value ({indicator_2})"].mean()
                    ) / merged_comparison[f"value ({indicator_2})"].std()

                # Plot the comparison
                st.write(f"### Comparison of {indicator_1} and {indicator_2}")
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(pd.to_datetime(merged_comparison["date"]), merged_comparison[f"value ({indicator_1})"], label=indicator_1)
                ax.plot(pd.to_datetime(merged_comparison["date"]), merged_comparison[f"value ({indicator_2})"], label=indicator_2)
                ax.set_xlabel("Date")
                ax.set_ylabel("Value (Normalized)" if normalize_data else "Value")
                ax.set_title(f"{indicator_1} vs {indicator_2}")
                ax.legend()
                plt.xticks(rotation=45)
                st.pyplot(fig)
        else:
            st.error("One or both of the selected data files are missing.")



# Tab 4: AI-Generated Insights
with tab4:
    st.subheader("AI-Generated Insights")
    st.write("The insights below are generated using only the data from the selected date range (quarterly).")

    # Reload button
    if st.button("Reload Summary"):
        # Clear stored summary in session state
        if "summary" in st.session_state:
            del st.session_state["summary"]

    # Load and process all indicators
    all_data = {}
    for name, filename in indicators.items():
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            data = pd.read_csv(file_path, parse_dates=["date"])
            data.set_index("date", inplace=True)

            # Resample all data to quarterly frequency
            filtered_data = data.loc[start_date:end_date].resample("Q").mean()
            all_data[name] = filtered_data

    # Generate concise summary function
    def generate_summary(all_data):
        summary_texts = []
        for name, data in all_data.items():
            if not data.empty:
                data_snippet = data.to_csv(index=True)
                prompt = (
                    f"Provide a concise 5-sentence analysis of trends in {name} for the period {start_date} to {end_date}, "
                    f"highlighting major trends, key events, and recent changes. Data:\n{data_snippet}"
                )

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are an economic analyst providing concise summaries of data trends."},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.7,
                        max_tokens=250,
                    )
                    summary_texts.append(f"**{name}:** {response.choices[0].message.content.strip()}")
                except Exception as e:
                    summary_texts.append(f"**{name}:** An error occurred while generating the summary: {str(e)}")
        return "\n\n".join(summary_texts)

    # Store the summary in Streamlit session state to avoid recomputation
    if "summary" not in st.session_state:
        if all_data:
            st.session_state["summary"] = generate_summary(all_data)
        else:
            st.session_state["summary"] = "No data available in the selected time range for generating a summary."

    # Display the stored summary
    st.subheader("Summary")
    st.write(st.session_state["summary"])

    # Tab 4: AI-Generated Insights
with tab4:
    st.subheader("AI-Generated Insights")
    st.write("The insights below are generated using only the data from the selected date range.")

    # Load all indicators
    all_data = {}
    for name, filename in indicators.items():
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            data = pd.read_csv(file_path, parse_dates=["date"])
            data.set_index("date", inplace=True)
            # Always use quarterly data for the AI insights
            filtered_data = data.loc[start_date:end_date].resample("Q").mean()  # Quarterly
            all_data[name] = filtered_data

    # Generate concise summary
    def generate_summary(all_data):
        summary_texts = []
        for name, data in all_data.items():
            if not data.empty:
                data_snippet = data.to_csv(index=True)
                prompt = (
                    f"Provide a concise analysis of trends in {name} for the period {start_date} to {end_date}, "
                    f"highlighting major trends, key events, and recent changes. Data:\n{data_snippet}"
                )

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are an economic analyst providing concise summaries of data trends."},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.7,
                        max_tokens=250,
                    )
                    summary_texts.append(f"**{name}:** {response.choices[0].message.content.strip()}")
                except Exception as e:
                    summary_texts.append(f"**{name}:** An error occurred while generating the summary: {str(e)}")
        return "\n\n".join(summary_texts)

    # Generate Summary
    st.subheader("Summary")
    if all_data:
        summary = generate_summary(all_data)
        st.write(summary)
    else:
        st.error("No data available in the selected time range for generating a summary.")

    # Q&A Section
    st.subheader("Ask a Question")
    if "qa_response" not in st.session_state:
        st.session_state.qa_response = None  # Store the last response
    if "qa_question" not in st.session_state:
        st.session_state.qa_question = ""  # Store the last question

    # Input for question
    user_question = st.text_input(
        "Ask a question about the macroeconomic data (in the selected date range):",
        key="user_question_input"
    )

    # Handle question submission
    if st.button("Submit"):
        if user_question.strip() != "":
            st.session_state.qa_question = user_question  # Update the session state with the new question
            # Send the new question to GPT-4o
            all_data_snippet = "\n".join([data.to_csv(index=True) for data in all_data.values()])
            prompt = (
                f"Answer the following question using the provided macroeconomic data for the range {start_date} to {end_date} in 8 or less sentences:\n"
                f"{user_question}\n\nData:\n{all_data_snippet}"
            )
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an economic analyst answering questions based on provided data."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=300,
                )
                st.session_state.qa_response = response.choices[0].message.content.strip()  # Store the response
            except Exception as e:
                st.session_state.qa_response = f"An error occurred while answering the question: {str(e)}"
        else:
            st.error("Please enter a valid question.")

    # Display the latest response
    if st.session_state.qa_response:
        st.write(st.session_state.qa_response)
