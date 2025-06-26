import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import warnings
warnings.filterwarnings('ignore')

# === 1. Load Data ===
def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    print("Data loaded successfully. Shape:", df.shape)
    return df

# === 2. Feature Engineering ===
def create_features(df):
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.weekday
    df['day_of_year'] = df['date'].dt.dayofyear
    return df

# === 3. Preprocess Data ===
def preprocess(df):
    df = df.dropna()
    df = df[df['temp'] < 60]  # remove outliers (e.g., extreme temp values)
    features = ['humidity', 'pressure', 'wind_speed', 'month', 'day', 'weekday']
    X = df[features]
    y = df['temp']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler

# === 4. Train Models ===
def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)

    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)

    # Evaluation
    print("\nLinear Regression Results:")
    evaluate_model(y_test, y_pred_lr)

    print("\nRandom Forest Results:")
    evaluate_model(y_test, y_pred_rf)

    return lr, rf

# === 5. Evaluation Function ===
def evaluate_model(y_true, y_pred):
    print("MAE: ", mean_absolute_error(y_true, y_pred))
    print("MSE: ", mean_squared_error(y_true, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_true, y_pred)))
    print("R2 Score:", r2_score(y_true, y_pred))

# === 6. Visualize Predictions ===
def visualize_predictions(model, X, y, title="Model Predictions"):
    y_pred = model.predict(X)
    plt.figure(figsize=(10, 5))
    plt.scatter(y, y_pred, alpha=0.5)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
    plt.xlabel('Actual Temperature')
    plt.ylabel('Predicted Temperature')
    plt.title(title)
    plt.grid(True)
    plt.show()

# === 7. Cross-Validation ===
def cross_validation(model, X, y):
    scores = cross_val_score(model, X, y, scoring='r2', cv=5)
    print("Cross-validation R2 scores:", scores)
    print("Mean R2:", scores.mean())

# === 8. Hyperparameter Tuning ===
def tune_random_forest(X, y):
    params = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    }
    rf = RandomForestRegressor(random_state=42)
    grid = GridSearchCV(rf, params, cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
    grid.fit(X, y)
    print("Best Parameters:", grid.best_params_)
    return grid.best_estimator_

# === 9. Predict for Future Sample ===
def predict_sample(model, scaler):
    sample = pd.DataFrame([{
        'humidity': 45,
        'pressure': 1012,
        'wind_speed': 3.5,
        'month': 6,
        'day': 26,
        'weekday': 2
    }])
    sample_scaled = scaler.transform(sample)
    prediction = model.predict(sample_scaled)
    print("Predicted temperature:", round(prediction[0], 2), "°C")

# === 10. Main ===
def main():
    filepath = "weather.csv"
    df = load_data(filepath)
    df = create_features(df)
    X_scaled, y, scaler = preprocess(df)

    lr_model, rf_model = train_models(X_scaled, y)

    print("\n--- Cross Validation ---")
    cross_validation(rf_model, X_scaled, y)

    print("\n--- Tuning Random Forest ---")
    best_rf = tune_random_forest(X_scaled, y)

    print("\n--- Final Evaluation ---")
    y_pred = best_rf.predict(X_scaled)
    evaluate_model(y, y_pred)
    visualize_predictions(best_rf, X_scaled, y, title="Best Random Forest Model")

    print("\n--- Sample Prediction ---")
    predict_sample(best_rf, scaler)


if __name__ == "__main__":
    main()
