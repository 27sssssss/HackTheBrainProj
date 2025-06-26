import requests
from datetime import datetime, timedelta

GDACS_API = "https://www.gdacs.org/gdacsapi/api/Events/geteventlist/latest"


EVENT_TYPE_MAP = {
    "EQ": ("Earthquake", "#FF3333"),       
    "TC": ("Tropical Cyclone", "#00CCCC"), 
    "FL": ("Flood", "#3366FF"),            
    "VO": ("Volcano", "#FF9933"),         
    "DR": ("Drought", "#9933FF"),          
    "WF": ("Wildfire", "#CC0000"),         
    "TS": ("Tsunami", "#3399FF"),          
}

def fetch_gdacs_events(limit_days=30):

    response = requests.get(GDACS_API)
    data = response.json()

    if "features" not in data:
        raise Exception("empty response GDACS")

    events = []
    for item in data["features"]:
        prop = item.get("properties", {})
        geom = item.get("geometry", {})
        coords = geom.get("coordinates", [None, None])
        
        todate = prop.get("todate", None)
        if todate:
            event_date = datetime.strptime(todate[:10], "%Y-%m-%d")
            if datetime.utcnow() - event_date > timedelta(days=limit_days):
                continue

        event_code = prop.get("eventtype", "")
        event_name, color = EVENT_TYPE_MAP.get(event_code, ("Unknown", "#999999"))

        events.append({
            "date": prop.get("todate", ""),
            "event_type": event_name,
            "color": color,
            "severity": prop.get("alertlevel", ""),
            "magnitude": prop.get("magnitude", 0),
            "lat": coords[1],
            "lng": coords[0]
        })

    return events

if __name__ == "__main__":
    events = fetch_gdacs_events()
    print("List of Disasters:\n")
    for e in events:
        print(e,',')
