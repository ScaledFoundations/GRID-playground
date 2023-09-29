import airgen
import time
client = airgen.MultirotorClient()
client.confirmConnection()

client.moveByVelocityAsync(0, -5, 0, 120)
client.simEnableWeather(False)

# Iterate over hour of day from 12 to 23 and then 0 to 12

for hour in range(12, 24):
    for minute in range(0, 60):
        print(f"2023-09-08 {hour}:{minute}:00")
        client.simSetTimeOfDay(True, f"2023-09-08 {hour}:{str(minute).zfill(2)}:00", True)
        time.sleep(0.016)
for hour in range(0, 12):
    for minute in range(0, 60):
        print(f"2023-09-08 {hour}:{minute}:00")
        client.simSetTimeOfDay(True, f"2023-09-08 {hour}:{str(minute).zfill(2)}:00", True)
        time.sleep(0.016)
    
client.simEnableWeather(True)

for i in range(0, 10):
    client.simSetWeatherParameter(airgen.WeatherParameter.Rain, i/10)
    time.sleep(0.1)
for i in range(10, 0, -1):
    client.simSetWeatherParameter(airgen.WeatherParameter.Rain, i/10)
    time.sleep(0.1)
for i in range(0, 10):
    client.simSetWeatherParameter(airgen.WeatherParameter.Snow, i/10)
    client.simSetWeatherParameter(airgen.WeatherParameter.Fog, i/10)
    time.sleep(0.1)
for i in range(10, 0, -1):
    client.simSetWeatherParameter(airgen.WeatherParameter.Snow, i/10)
    client.simSetWeatherParameter(airgen.WeatherParameter.Fog, i/10)
    time.sleep(0.1)
for i in range(0, 10):
    client.simSetWeatherParameter(airgen.WeatherParameter.Dust, i/10)
    time.sleep(0.1)
for i in range(10, 0, -1):
    client.simSetWeatherParameter(airgen.WeatherParameter.Dust, i/10)
    time.sleep(0.1)


client.simSetWind(airgen.Vector3r(5.0, 0, 0))
time.sleep(5)
client.simSetWind(airgen.Vector3r(0, 0, 0))