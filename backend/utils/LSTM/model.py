import numpy as np
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import os

MODEL_PATH = "disaster_lstm_model.h5"
scaler = MinMaxScaler()


def prepare_data(csv_path, time_steps=24):
    df = pd.read_csv(csv_path)
    df = df.dropna()
    df = df.sort_values("date")

    features = df[['temperature', 'precipitation', 'humidity']].values
    labels = df['label'].values 

    features_scaled = scaler.fit_transform(features)

    X, y = [], []
    for i in range(len(features_scaled) - time_steps):
        X.append(features_scaled[i:i + time_steps])
        y.append(labels[i + time_steps])

    return np.array(X), np.array(y)


def update_model(csv_path):
    X, y = prepare_data(csv_path)

    if os.path.exists(MODEL_PATH):
        print("Loading model...")
        model = load_model(MODEL_PATH)
    else:
        print("Creating LSTM model...")
        model = Sequential()
        model.add(LSTM(64, input_shape=(X.shape[1], X.shape[2])))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print("Feeding...")
    model.fit(X, y, epochs=2, batch_size=32, verbose=1)

    print("Saving model...")
    model.save(MODEL_PATH)



def predict_risk(csv_path, time_steps=24):
    df = pd.read_csv(csv_path).dropna()
    df = df.sort_values("date")

    recent = df[['temperature', 'precipitation', 'humidity']].tail(time_steps).values
    recent_scaled = scaler.transform(recent)
    input_seq = np.expand_dims(recent_scaled, axis=0)

    model = load_model(MODEL_PATH)
    prediction = model.predict(input_seq)

    return prediction[0][0] 
