<p align="center">
  <img src="content/horizon.png" alt="Logo" />
</p>
<br>
<br>
<br>

### 🌍 Let me introduce Horizon — an AI-powered open-source platform designed to save lives

<br>

https://github.com/user-attachments/assets/a993361e-b00c-48a3-a043-a2fd0bc24b3c

<br>

## 🛰️ Horizon: Predict. Prevent. Protect.

**Horizon is an AI-powered, open-source platform that predicts climate disasters before they happen.**\
By analyzing decades of global satellite data, environmental signals, and real-time disaster feeds, Horizon delivers early warnings and risk forecasts directly to communities at risk — helping them prepare, respond, and stay safe. From wildfires and hurricanes to floods and earthquakes, Horizon empowers people to act before it’s too late.

## 🔧 Features

- ✅ **NASA POWER & GEE integration**: Load climate indicators (temperature, precipitation, NDVI, LST)
- 🌪️ **GDACS API**: Fetch latest disaster records (earthquakes, floods, storms, etc.)
- 🤖 **LSTM Model**: Predict the probability of a disaster based on historical sequences
- 🧠 **Incremental Learning**: Continuously improve model with new daily data
- 📦 **Modular**: Easy to scale or customize input sources

# 🧠 GeoAI Training Flow

This system collects real-time weather and satellite data from **NASA POWER**, **Google Earth Engine**, and global disaster reports via **GDACS API**. It merges and labels this data to train an **LSTM neural network**, which learns to detect early signs of natural disasters based on past climate patterns. The model is updated regularly and predicts the likelihood of upcoming disasters using today’s conditions.

```

                        ┌────────────────────────────┐
                        │     Daily Data Pipeline    │
                        └────────────┬───────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
┌────────────────┐         ┌─────────────────────┐      ┌────────────────────┐
│ NASA POWER API │         │ Google Earth Engine │      │     GDACS API      │
│ - Temperature  │         │ - NDVI              │      │ - Disasters (type) │
│ - Precipitation│         │ - LST               │      │ - Location, date   │
└────────────────┘         └─────────────────────┘      └────────────────────┘
        │                            │                            │
        └────────────┬───────────────┴──────────────┬─────────────┘
                     ▼                             ▼
            ┌────────────────────────────┐   ┌────────────────────────┐
            │ Climate + Satellite Data   │   │ Disaster Event Metadata│
            │ - Aligned by location/date │   │ - Type, severity, etc. │
            └────────────┬───────────────┘   └──────────┬─────────────┘
                         ▼                              ▼
                  ┌──────────────────────────────────────────┐
                  │      Data Fusion & Labeling Engine       │
                  │ - Merge data by location & time          │
                  │ - Assign label: Disaster = 1 / No = 0    │
                  └────────────────────────┬─────────────────┘
                                           ▼
                             ┌────────────────────────────┐
                             │ Sequence Generator (14-day)│
                             │ - Prepare X (features)     │
                             │ - Prepare y (labels)       │
                             └────────────┬───────────────┘
                                          ▼
                            ┌───────────────────────────────┐
                            │     LSTM Model Trainer        │
                            │ - Train or fine-tune model    │
                            └────────────────────┬──────────┘
                                                 ▼
                                 ┌────────────────────────────┐
                                 │   Daily Prediction Engine  │
                                 │ - Use today’s data to      │
                                 │   predict tomorrow’s risk  │
                                 └────────────────────────────┘

```

## 📊 Data Sources

- [NASA POWER](https://power.larc.nasa.gov/)
- [Google Earth Engine](https://earthengine.google.com/)
- [GDACS Disaster API](https://www.gdacs.org/)

## How to run frontend

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.
You may also see any lint errors in the console.

```
npm test
```

Launches the test runner in the interactive watch mode.
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

```
npm run build
```

Builds the app for production to the `build` folder.
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

```
npm run eject
```

## How to run backend

Use Python 3.10

In the backend directory:

Create an envirometn

```
python -m venv env
source env/bin/activate     # Mac/Linux
env\Scripts\activate        # Windows
```

Install libs

```
pip install -r requirements.txt
```

Than run it 

```
uvicorn main:app --reload
```
How to check Swagger

```
http://localhost:8000/docs
```
## 🧠 Authors

Project by:

- Viktor Makarov
- Semen Vinnik
- Dmytro Litvinov

at HackTheBrain 2025 💥

----
