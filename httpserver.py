from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mysql.connector
import time

hostname = "localhost"
port = 8080

time.sleep(5)

class weatherHTTP(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>HELLO</h1></body></html>", "utf-8"))

# Database enviroment
mydb = mysql.connector.connect(
  host=os.environ['MYSQL_HOST'],
  user=os.environ["MYSQL_USER"],
  password=os.environ["MYSQL_PASSWORD"],
  db=os.environ["MYSQL_DB"]
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM WeatherData ORDER BY QueryTime DESC")

server = HTTPServer((hostname, port), weatherHTTP)
# print("server is running")
server.serve_forever()
server.server_close()