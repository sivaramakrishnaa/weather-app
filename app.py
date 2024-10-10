from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)


#def k_to_c(temp):
   # return temp - 273.15

# Convert m/s to km/h
def mps_to_kmph(mps):
    return mps * 3.6

def degrees_to_direction(degrees):
    directions = ['North', 'North East', 'East', 'South East', 'South', 'South West', 'West', 'North West']
    index = round(degrees / 45) % 8
    return directions[index]

def unix_to_local_time(unix_time):
    local_time = datetime.datetime.fromtimestamp(unix_time)
    return local_time.strftime("%H:%M:%S")

def convert_12_format(s):
    temp = int(s[:2]) - 12
    new_string = str(temp) + s[2:]
    return new_string

def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        ## to get lat & lan
        coord = data['coord']
        longitude = coord['lon']
        latitude = coord['lat']

        ## to get description
        weather = data['weather']
        desc = weather[0]['description']
        icon = weather[0]['icon']

        ## convert kelvin to celcius
        main = data['main']
        temp = main['temp']
        temperature = temp ##k_to_c(temp)

        like = main['feels_like']
        feels_like = like ##k_to_c(like)

        pressure = main['pressure']
        humidity = main['humidity']

        ## to get wind data
        wind_data = data['wind']
        speed = wind_data['speed'] 
        print(speed)
        wind_speed = mps_to_kmph(speed)
        

        direction = wind_data['deg']
        wind_direction = degrees_to_direction(direction)

        ## to get sys data
        
        sys_data = data['sys']
        sunrise_data = sys_data['sunrise']
        sunrise = unix_to_local_time(sunrise_data)
        sunset_data = sys_data['sunset']
        sunset = unix_to_local_time(sunset_data)
        sunset = convert_12_format(sunset)

        weather_data = {
                'city': city,
                'temperature': temperature,
                'feels_like': feels_like,
                'longitude':longitude,
                'latitude':latitude,
                'humidity': humidity,
                'pressure': pressure,
                'description': desc,
                'wind_speed': wind_speed,
                'wind_direction': wind_direction,
                'sunrise': sunrise,
                'sunset': sunset,
                'icon': icon
            }
    else:
        weather_data = {'error': 'City Not Found!'}

    return weather_data

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        api_key = '7a9aacd777771f61b4b51d27af857ae6'
        weather_data = get_weather_data(city,api_key)
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)