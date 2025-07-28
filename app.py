from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    answer = None
    if request.method == 'POST':
        city = request.form['city']
        question = request.form['question'].lower()
        data = get_weather(city)

        if data.get("cod") != 200:
            answer = f"Error: {data.get('message', 'City not found.')}"
        else:
            weather = data.get('weather', [{}])[0]
            main = data.get('main', {})
            wind = data.get('wind', {})

            if "temperature" in question:
                answer = f"The temperature is {main.get('temp')}°C."
            elif "wind" in question:
                answer = f"The wind speed is {wind.get('speed')} m/s."
            elif "cloudy" in question or "sunny" in question:
                answer = f"Current condition: {weather.get('description')}"
            else:
                answer = "Sorry, I can only answer basic weather questions."

    return render_template('index.html', answer=answer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
