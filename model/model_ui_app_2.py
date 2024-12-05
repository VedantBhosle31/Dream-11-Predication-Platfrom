import streamlit as st
from datetime import datetime
import pandas as pd
import subprocess
import os
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

# Page Configuration
st.set_page_config(
    page_title="Model UI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("📊 Model User Interface")
st.write("""
Welcome to the **Model UI**. Select your desired date ranges from the sidebar to process and view model results.
""")

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
    training_start_str = training_start_date.strftime('%Y-%m-%d')
    training_end_str = training_end_date.strftime('%Y-%m-%d')
    testing_start_str = testing_start_date.strftime('%Y-%m-%d')
    testing_end_str = testing_end_date.strftime('%Y-%m-%d')

    # Define the command to run the script with arguments
    util_location = os.path.join('model', 'train_and_predict_model.py')
    command = [
        "python", util_location,
        training_start_str, training_end_str,
        testing_start_str, testing_end_str
    ]
    
    # Run the script using subprocess
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Assuming the script generates a predictions.csv file
        result_path = os.path.join('data','output_files','final_result.csv') # Adjust path if necessary
        
        if os.path.exists(result_path):
            st.success("✅ Data successfully processed!")
            
            # Display options for the user
            st.write("### 📊 Model Results")
            with st.expander("🔍 View Results"):
                result_df = pd.read_csv(result_path)  # Read the CSV into a dataframe
                st.dataframe(result_df)  # Display the DataFrame
                
                
            # MAE Histogram

            data = result_df['Total points MAE']

            st.write("### Histogram Visualization")

            st.write("""
            This app generates a histogram for a given dataset.
            Customize the appearance and bins using the controls below.
            """)

            # Sidebar controls
            bins = st.sidebar.slider("Number of Bins", min_value=3, max_value=15, value=6)
            color = st.sidebar.color_picker("Pick a Bar Color", "#1f77b4")
            edge_color = st.sidebar.color_picker("Pick an Edge Color", "#000000")

            # Create and decorate the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data, bins=bins, color=color, edgecolor=edge_color)
            ax.set_title("Histogram of Values", fontsize=16)
            ax.set_xlabel("Total Points MAE", fontsize=12)
            ax.set_ylabel("Frequency", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)

            # Display the plot in Streamlit
            st.pyplot(fig)
            
            
            
            # Optional download button
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="model_results.csv",
                mime="text/csv"
            )
        else:
            st.error("❌ Could not find the predictions.csv file. Please try again.")
    
    except subprocess.CalledProcessError as e:
        st.error(f"Error while running the script: {e}")
