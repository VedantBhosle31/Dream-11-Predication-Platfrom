import pandas as pd
import yaml
import subprocess
import os
import requests
import time
import numpy as np
import warnings
import math
from datetime import datetime
import zipfile

warnings.filterwarnings("ignore")


def download_file(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    file_name = url.split("/")[-1]
    file_path = os.path.join(output_folder, file_name)

    print(f"Downloading {file_name} from {url}...")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded {file_name} to {file_path}")
    else:
        print(
            f"Failed to download {file_name}. HTTP Status Code: {response.status_code}"
        )
    return


def download_cricsheet_data():
    female_url = "https://cricsheet.org/downloads/all_female.zip"
    male_url = "https://cricsheet.org/downloads/all_male.zip"

    output_directory = os.path.join("data", "raw", "cricsheet_data")

    download_file(female_url, output_directory)
    download_file(male_url, output_directory)
    return


def unzip_file(zip_path, extract_to):
    if not os.path.exists(zip_path):
        print(f"ZIP file does not exist: {zip_path}")
        return

    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted {zip_path} to {extract_to}")
    return


def unzip():
    folder = os.path.join("data", "raw", "cricsheet_data")
    male_fol = os.path.join(folder, "all_male")
    female_fol = os.path.join(folder, "all_female")
    os.makedirs(male_fol, exist_ok=True)
    os.makedirs(female_fol, exist_ok=True)
    unzip_file(os.path.join(folder, "all_male.zip"), male_fol)
    unzip_file(os.path.join(folder, "all_female.zip"), female_fol)
    return


def sort_helper(gender):
    date_file_pair = []

    if gender == "female":
        location = os.path.join("data", "raw", "cricsheet_data", "all_female")
        output_name = "sorted_acc_to_date_and_format_female.csv"
    else:
        location = os.path.join("data", "raw", "cricsheet_data", "all_male")
        output_name = "sorted_acc_to_date_and_format_male.csv"

    print("Total number of files for " + gender + ": " + str(len(os.listdir(location))))

    i = 0
    for filename in os.listdir(location):
        i += 1
        if i % 1000 == 0:
            print("on " + str(i) + "th file")
        if filename.endswith(".yaml"):
            dict = yaml.load(open(os.path.join(location, filename)), yaml.Loader)
            date = dict["info"]["dates"][0]
            format = ""
            try:
                format = dict["info"]["match_type"]
            except:
                format = "None"
            if type(date) == str:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            date_file_pair.append([date, filename, format])
    print("Done for " + gender)
    date_file_pair.sort(key=lambda x: x[0])

    import pandas

    df = pd.DataFrame(date_file_pair, columns=["date", "filename", "format"])

    output_file = os.path.join("data", "interim", output_name)
    df.to_csv(output_file, index=False)
    return


def sort_dataset():
    sort_helper("male")
    sort_helper("female")
    return


if __name__ == "__main__":
    download_cricsheet_data()
    unzip()
    sort_dataset()
