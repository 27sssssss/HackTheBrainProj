# weather_interface.py

from mml_forcast import load_data, create_features, preprocess, train_models, predict_sample
import pandas as pd

def run_interface():
    print("=== Welcome to Weather Predictor Interface ===\n")
    
    filepath = "weather.csv"
    
    try:
        # 1. Загрузка данных
        df = load_data(filepath)
    except FileNotFoundError:
        print(f"Error: Файл '{filepath}' не найден. Убедитесь, что он находится в той же директории.")
        return

    # 2. Создание признаков
    df = create_features(df)

    # 3. Предобработка
    X_scaled, y, scaler = preprocess(df)

    # 4. Обучение моделей
    lr_model, rf_model = train_models(X_scaled, y)

    print("\nМодель успешно обучена. Готов к предсказаниям!\n")

    # 5. Пользовательский ввод
    while True:
        answer = input("\nХотите предсказать температуру для новой даты? (yes/no): ").strip().lower()
        if answer != 'yes':
            print("Выход из программы. Спасибо за использование.")
            break

        try:
            # Ввод параметров
            humidity = float(input("Введите влажность (в %): "))
            pressure = float(input("Введите давление (в hPa): "))
            wind_speed = float(input("Введите скорость ветра (м/с): "))
            month = int(input("Введите номер месяца (1-12): "))
            day = int(input("Введите день месяца (1-31): "))
            weekday = int(input("Введите день недели (0 — Пн, 6 — Вс): "))

            # Создание DataFrame для предсказания
            user_sample = pd.DataFrame([{
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'month': month,
                'day': day,
                'weekday': weekday
            }])

            # Масштабирование
            user_scaled = scaler.transform(user_sample)

            # Предсказание
            prediction = rf_model.predict(user_scaled)
            print(f"\n🌤 Прогнозируемая температура: {round(prediction[0], 2)} °C")

        except Exception as e:
            print("Ошибка ввода данных:", e)
            continue

if __name__ == "__main__":
    run_interface()
