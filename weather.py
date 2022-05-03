import requests
import mysql.connector
import os
import time

# API elements
API_KEY = "5a12f688ca668ab2b8e7ef2333abadae"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

time.sleep(5)

# Database enviroment
mydb = mysql.connector.connect(
  host=os.environ['MYSQL_HOST'],
  user=os.environ["MYSQL_USER"],
  password=os.environ["MYSQL_PASSWORD"],
  db=os.environ["MYSQL_DB"]
)

# Create database
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS todos")

# Creating tables
mycursor.execute("CREATE TABLE IF NOT EXISTS WeatherData (City VARCHAR(50), Description VARCHAR(50), Temperature smallint, QueryTime INT UNSIGNED)")

cities = ["Los Angeles", "Warsaw", "Seul"]

while(True):
  for city in cities:
      requests_url = f"{BASE_URL}?appid={API_KEY}&q={city}"
      response = requests.get(requests_url)

      if response.status_code == 200:
          data = response.json()
          weather = data["weather"][0]["description"]
          temperature = round(data["main"]["temp"] - 273.15, 2)

          # insert data
          mycursor.execute("INSERT INTO WeatherData (City, Description, Temperature, QueryTime) VALUES (%s,%s,%s,%s)", (city, weather, temperature, time.time()))
          mydb.commit()
      else:
          print("An error occured")
  
  time.sleep(300)

mycursor.close()
mydb.close()
