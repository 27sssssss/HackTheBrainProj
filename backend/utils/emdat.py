import pandas as pd
import os
from typing import List, Dict

def parse_emdat_excel_local(filepath: str) -> List[Dict]:
    df = pd.read_excel(filepath)  # <-- читаем как Excel

    print("📌 Найденные колонки:", df.columns.tolist())

    # Переименуем для унификации
    df = df.rename(columns={
        "Start Year": "Year",
        "Total Affected": "Affected"
    })

    relevant_columns = ["Disaster Type", "Country", "Year", "Total Deaths", "Affected"]
    df = df[relevant_columns].dropna()

    df["label"] = ((df["Total Deaths"] > 1000) | (df["Affected"] > 50000)).astype(int)

    return df.to_dict(orient="records")


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    path = "241204_emdat_columns.xlsx"

    events = parse_emdat_excel_local(path)

    for e in events:
        print(e, ',')
