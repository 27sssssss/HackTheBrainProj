<p align="center">
  <img src="content/horizon.png" alt="Logo" />
</p>
<br>
<br>
<br>

### 🌍 Let me introduce Horizon — an AI-powered open-source platform designed to save lives

<div align="center">
    <figure class="video_container">
    <video controls="true" allowfullscreen="true">
    <source src="content/demo.mp4" type="video/mp4">
    </video>
    </figure>
</div>

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

## 🧠 Authors

Project by:

- Viktor Makarov
- Semen Vinnik
- Dmytro Litvinov

at HackTheBrain 2025 💥

----
