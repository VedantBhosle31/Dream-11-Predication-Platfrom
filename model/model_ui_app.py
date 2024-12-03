import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Model UI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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
    # Check Date Validity
    if training_start_date > training_end_date or testing_start_date > testing_end_date:
        st.error("❗ Please ensure the start date is earlier than the end date.")
    else:
        # Fetch data from the backend (Replace with your API endpoint)
        api_url = "http://your-backend-api.com/get-results"
        payload = {
            "training_start": training_start_date.strftime('%Y-%m-%d'),
            "training_end": training_end_date.strftime('%Y-%m-%d'),
            "testing_start": testing_start_date.strftime('%Y-%m-%d'),
            "testing_end": testing_end_date.strftime('%Y-%m-%d')
        }

        try:
            response = requests.get(api_url, params=payload)
            response.raise_for_status()
            data = response.json()  # Ensure the API returns JSON

            # Display Results
            st.success("✅ Data successfully fetched!")
            st.write("### 📊 Model Results")
            df = pd.DataFrame(data)  # Convert JSON data to DataFrame
            st.dataframe(df)

            # Allow CSV Download
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="model_results.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"❗ Failed to fetch data: {e}")

# Main Section
st.title("📊 Model User Interface")
st.write("""
Welcome to the **Model UI**. Select your desired date ranges from the sidebar to retrieve and view model results. 
You can also download the data as a CSV file for further analysis.
""")
st.image("https://via.placeholder.com/800x200?text=Your+Custom+Banner", use_container_width=True)
