import requests
from datetime import datetime

def fetch_nasa_power_data(lat, lon, start_date, end_date):
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,RH2M,PRECTOTCORR", 
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "properties" not in data or "parameter" not in data["properties"]:
        raise Exception("Ошибка: некорректный ответ от API.")

    raw_data = data["properties"]["parameter"]

    required_params = ["T2M", "PRECTOTCORR", "RH2M"]
    for p in required_params:
        if p not in raw_data:
            raise Exception(f"Параметр {p} отсутствует в ответе API.")

    dates = list(raw_data["T2M"].keys())
    result = []

    for date in dates:
        result.append({
            "date": datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d"),
            "temperature": raw_data["T2M"][date],
            "precipitation": raw_data["PRECTOTCORR"][date],
            "humidity": raw_data["RH2M"][date]
        })

    return result

if __name__ == "__main__":
    data = fetch_nasa_power_data(
        lat=55.75,  
        lon=37.61,
        start_date="20220101",
        end_date="20221231"
    )

    from pprint import pprint
    pprint(data[:5]) 
