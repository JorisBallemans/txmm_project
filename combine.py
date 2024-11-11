import glob, os, config
import pandas as pd

def get_all_csvs(folder):
    csv_files = []
    for file in os.listdir(folder):
        csv_files.append(file)
    return [f"{folder}{csv_file}" for csv_file in csv_files if csv_file.endswith(".csv")]

def main():
    csv_files = get_all_csvs(config.OUTPUT_FOLDER)
    dataframes = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv("hoppa.csv", index= False)

if __name__ == "__main__":
    main()