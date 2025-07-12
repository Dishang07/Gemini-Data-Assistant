import pandas as pd
import os

def get_dataset_schema():
    dataset_path = os.path.join("backend", "personality_datasert.xlsx")
    df = pd.read_excel(dataset_path)
    schema = list(df.columns)
    return schema
