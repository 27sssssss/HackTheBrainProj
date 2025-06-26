import pandas as pd
import os

from typing import List, Dict

def parse_emdat_excel_local(filepath: str) -> List[Dict]:
    df = pd.read_excel(filepath) 
    print("📌 New columns:", df.columns.tolist())

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
    path = os.path.join(current_dir, 'LSTM', 'data', '241204_emdat_archive.xlsx')

    events = parse_emdat_excel_local(path)

    for e in events:
        print(e, ',')

    output_path = os.path.join(current_dir, 'LSTM', 'data', 'events.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(events)} events to {output_path}")
