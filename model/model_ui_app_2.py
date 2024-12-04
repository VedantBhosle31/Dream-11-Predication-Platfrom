import streamlit as st
from datetime import datetime
import pandas as pd
import subprocess
import os

# Page Configuration
st.set_page_config(
    page_title="Model UI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("📅 Date Range Selection")
st.sidebar.write("Please select the training and testing date ranges.")

# Inputs
st.sidebar.subheader("Training Dates")
training_start_date = st.sidebar.date_input("From", value=datetime(2023, 1, 1))
training_end_date = st.sidebar.date_input("To", value=datetime(2023, 6, 30))

st.sidebar.subheader("Testing Dates")
testing_start_date = st.sidebar.date_input("From", value=datetime(2023, 7, 1))
testing_end_date = st.sidebar.date_input("To", value=datetime(2023, 12, 31))

# Submit Button
if st.sidebar.button("🔍 Fetch Results"):
    # Convert dates to strings for command line arguments
    training_start_str = training_start_date.strftime("%Y-%m-%d")
    training_end_str = training_end_date.strftime("%Y-%m-%d")
    testing_start_str = testing_start_date.strftime("%Y-%m-%d")
    testing_end_str = testing_end_date.strftime("%Y-%m-%d")

    # Define the command to run the script with arguments
    command = [
        "python",
        "util.py",
        training_start_str,
        training_end_str,
        testing_start_str,
        testing_end_str,
    ]

    # Run the script using subprocess
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Assuming the script generates a predictions.csv file
        predictions_file = "Final_Result.csv"  # Adjust path if necessary

        if os.path.exists(predictions_file):
            st.success("✅ Data successfully processed!")
            st.write("### 📊 Model Results")
            result_df = pd.read_csv(predictions_file)  # Read the CSV into a dataframe
            st.dataframe(result_df)

            # Allow CSV Download
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="model_results.csv",
                mime="text/csv",
            )
        else:
            st.error("❌ Could not find the predictions.csv file. Please try again.")

    except subprocess.CalledProcessError as e:
        st.error(f"Error while running the script: {e}")
