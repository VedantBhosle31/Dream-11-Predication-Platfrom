import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from concurrent.futures import ThreadPoolExecutor

# PostgreSQL connection details
db_config = {
    "dbname": "",
    "user": "",
    "password": "",
    "host": "",
    "port": 5432 
}

csv_dir = "/content/drive/MyDrive/data"

# Function to create and populate tables from CSV
def create_and_populate_table(csv_file):
    # Create a new database connection for each thread
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to PostgreSQL for file {csv_file}: {e}")
        return

    try:
        # Load CSV into a DataFrame
        df = pd.read_csv(csv_file)

        # Sanitize column names (replace invalid characters)
        df.columns = df.columns.str.replace(r'^\d', 'col_\g<0>', regex=True)
        df = df.drop(columns=[col for col in df.columns if ':' in col])

        # Infer table name from file name (without extension)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]

        # Generate CREATE TABLE SQL statement
        columns = ", ".join(
            [f"{col} {'TEXT' if dtype == 'object' else 'FLOAT'}" for col, dtype in zip(df.columns, df.dtypes)]
        )
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"

        # Create the table
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created successfully.")

        # Insert data into the table
        for _, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(row))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        print(f"Data from '{csv_file}' inserted into table '{table_name}'.")

    except Exception as e:
        print(f"Error processing file {csv_file}: {e}")
    finally:
        cursor.close()
        conn.close()

# List all CSV files
csv_files = [os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.endswith(".csv")]

# Use ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor() as executor:
    executor.map(create_and_populate_table, csv_files)

print("All CSV files processed successfully.")
