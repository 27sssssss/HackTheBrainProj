from mml_forcast import load_data, create_features, preprocess, train_models, predict_sample
import pandas as pd

def run_interface():
    print("=== Welcome to the Weather Predictor Interface ===\n")
    
    filepath = "weather.csv"
    
    try:
        # 1. Load data
        df = load_data(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found. Make sure it's in the same directory.")
        return

    # 2. Create features
    df = create_features(df)

    # 3. Preprocessing
    X_scaled, y, scaler = preprocess(df)

    # 4. Train models
    lr_model, rf_model = train_models(X_scaled, y)

    print("\nThe model has been trained successfully. Ready to make predictions!\n")

    # 5. User input loop
    while True:
        answer = input("\nWould you like to predict the temperature for a new date? (yes/no): ").strip().lower()
        if answer != 'yes':
            print("Exiting the program. Thank you for using the Weather Predictor.")
            break

        try:
            # User input
            humidity = float(input("Enter humidity (%): "))
            pressure = float(input("Enter pressure (hPa): "))
            wind_speed = float(input("Enter wind speed (m/s): "))
            month = int(input("Enter month number (1-12): "))
            day = int(input("Enter day of the month (1-31): "))
            weekday = int(input("Enter weekday number (0 = Mon, 6 = Sun): "))

            # Create DataFrame for prediction
            user_sample = pd.DataFrame([{
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'month': month,
                'day': day,
                'weekday': weekday
            }])

            # Scale input
            user_scaled = scaler.transform(user_sample)

            # Make prediction
            prediction = rf_model.predict(user_scaled)
            print(f"\n🌤 Predicted temperature: {round(prediction[0], 2)} °C")

        except Exception as e:
            print("Input error:", e)
            continue

if __name__ == "__main__":
    run_interface()
