#Import Libraries
import csv
import json
import requests


API_KEY = "df05e2cd8d86f66d6896165adc588333"

#Get the city name from the user
def get_city_name():
    city = input("Enter a City Name: ").strip()
    if city:
        return city

    print("City name cannot be empty. Please try again.")
    return None

#Get the weather data from the OpenWeatherMap API
def get_weather_data(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 404:
            print(f"City '{city}' not found. Please check the spelling and try again.")
            return None

        if response.status_code == 401:
            print("Invalid API key. Please check your API key and try again.")
            return None

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching weather data: {e}")
        return None

#Save the weather data to a CSV file
def save_to_csv(data):
    city = data["name"]
    country = data["sys"]["country"]
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    with open("city_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["City", "Country", "Temperature (°C)", "Description", "Humidity (%)"])
        writer.writerow([city, country, temperature, description, humidity])

#Read the weather data from the CSV file and display it
def read_csv_report():
    try:
        with open("city_data.csv", "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)

        print(f"\nNumber of cities in the report: {len(rows) - 1}")
        print("Cities and Temperatures:")

        for row in rows[1:]:
            print(f"{row[0]}: {row[2]} °C")
    except FileNotFoundError:
        print("The file 'city_data.csv' does not exist. Please ensure the file is created before reading it.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

#Main function to run the program
def main():
    city = get_city_name()
    if not city:
        return

    weather_data = get_weather_data(city)
    if not weather_data:
        print("No data to save to CSV.")
        return

    city_name = weather_data["name"]
    country = weather_data["sys"]["country"]
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    humidity = weather_data["main"]["humidity"]

    print("Weather Report:")
    print(f"City: {city_name}")
    print(f"Country: {country}")
    print(f"Temperature: {temperature} °C")
    print(f"Description: {description}")
    print(f"Humidity: {humidity}%")

    save_to_csv(weather_data)
    print(f"Weather Information for {city_name} has been saved to 'city_data.csv'.")
    read_csv_report()


if __name__ == "__main__":
    main()
