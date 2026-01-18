import pandas as pd
import os

def load_data(file_path: str) -> str:
    data = pd.read_csv(file_path)
    return save_data_to_txt(data, file_path)

def pd_df_to_txt(data: pd.DataFrame, output_path: str, filename: str) -> None:
    with open(output_path, 'w') as f:
        for index, row in data.iterrows():
            f.write(f"Record from: {filename}.csv, line: {index + 1}\n")
            for col in data.columns:
                f.write(f"{col}: {row[col]}\n")
            f.write("\n")

def save_data_to_txt(data: pd.DataFrame, path: str) -> str:
    filename = os.path.splitext(os.path.basename(path))[0]
    output_path = '../../storage/corpus/' + filename + '.txt'
    pd_df_to_txt(data, output_path, filename)
    return output_path

if __name__ == "__main__":
    path = '../../storage/data/cibc_finance_terms.csv'
    data = load_data(path)
