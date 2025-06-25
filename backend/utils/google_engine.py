import ee
import pandas as pd
from datetime import datetime


def init_gee():
    try:
        ee.Initialize()
    except Exception:
        ee.Authenticate()
        ee.Initialize()

def get_climate_features(lat, lon, start_date, end_date):

    point = ee.Geometry.Point([lon, lat])

    ndvi_col = ee.ImageCollection('MODIS/006/MOD13A2') \
        .filterDate(start_date, end_date) \
        .select('NDVI') \
        .filterBounds(point)

    lst_col = ee.ImageCollection('MODIS/006/MOD11A2') \
        .filterDate(start_date, end_date) \
        .select('LST_Day_1km') \
        .filterBounds(point)

    precip_col = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
        .filterDate(start_date, end_date) \
        .select('precipitation') \
        .filterBounds(point)

    def extract_feature(image, band_name, feature_name):
        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1000
        ).get(band_name)
        date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')
        return ee.Feature(None, {'date': date, feature_name: value})

    def collection_to_df(collection, band, name):
        features = collection.map(lambda img: extract_feature(img, band, name)).getInfo()
        rows = []
        for f in features['features']:
            p = f['properties']
            if p[name] is not None:
                rows.append({
                    'date': p['date'],
                    name: float(p[name]) / 10000 if name == 'ndvi' else float(p[name])
                })
        return pd.DataFrame(rows)

    df_ndvi = collection_to_df(ndvi_col, 'NDVI', 'ndvi')
    df_lst = collection_to_df(lst_col, 'LST_Day_1km', 'lst')
    df_precip = collection_to_df(precip_col, 'precipitation', 'precip')

    df = pd.merge(df_ndvi, df_lst, on='date', how='outer')
    df = pd.merge(df, df_precip, on='date', how='outer')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    return df


if __name__ == "__main__":
    init_gee()

    lat, lon = 35.0, 139.0  # Tokyo
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    df = get_climate_features(lat, lon, start_date, end_date)
    df.to_csv("climate_tokyo_2024.csv", index=False)
    print(df.head())