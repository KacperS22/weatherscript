from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mysql.connector
import time

hostname = "0.0.0.0"
port = 8080

time.sleep(5)

class weatherHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        mydb = mysql.connector.connect(
          host=os.environ['MYSQL_HOST'],
          user=os.environ["MYSQL_USER"],
          password=os.environ["MYSQL_PASSWORD"],
          db=os.environ["MYSQL_DB"]
        )
        mycursor = mydb.cursor()

        try:
          for result in mycursor.execute("SELECT * FROM WeatherData ORDER BY QueryTime DESC LIMIT 3", multi=True):
            if result.with_rows:
              self.wfile.write(bytes(str(result.fetchall()), "utf-8"))
        except RuntimeError:
          None
        
        mycursor.close()
        mydb.close()

server = HTTPServer((hostname, port), weatherHTTP)
server.serve_forever()
server.server_close()
