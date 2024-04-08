from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import psycopg2

# Database connection parameters
DB_NAME = "master"
DB_USER = "postgres"
DB_PASSWORD = "asdf"
DB_HOST = "localhost"

# Function to fetch data from PostgreSQL
def fetch_data():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cur = conn.cursor()

        # Example table name, replace with your actual table name
        table_name = "idnes_reality"

        # Fetch data from PostgreSQL
        cur.execute(f"SELECT title, price, image_urls FROM {table_name};")
        data = cur.fetchall()

        # Close cursor and connection
        cur.close()
        conn.close()

        return data
    except psycopg2.Error as e:
        print("Error fetching data from PostgreSQL:", e)
        return None

# HTTP request handler class
class RequestHandler(BaseHTTPRequestHandler):
    # Handler for GET requests
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Fetch data from PostgreSQL
            data = fetch_data()
            if data:
                self.wfile.write(bytes(render_html(data), "utf8"))
            else:
                self.wfile.write(bytes("Error fetching data from PostgreSQL", "utf8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("404 Not Found", "utf8"))

# Function to render HTML from fetched data
def render_html(data):
    html = "<!DOCTYPE html>\n<html>\n<head>\n<title>PostgreSQL Data</title>\n</head>\n<body>\n"
    html += "<h1>PostgreSQL Data</h1>\n<table border=\"1\">\n"
    html += "<tr><th>Title</th><th>Price</th><th>Image URLs</th></tr>\n"
    for row in data:
        html += "<tr>\n"
        html += f"<td>{row[0]}</td>\n"
        html += f"<td>{row[1]}</td>\n"
        html += "<td>\n<ul>\n"
        for url in row[2]:
            html += f"<li><img src=\"{url}\" width=\"100\" height=\"100\"></li>\n"
        html += "</ul>\n</td>\n</tr>\n"
    html += "</table>\n</body>\n</html>"
    return html



# Main function
def main():
    try:
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        print('Starting server on port 8000...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the server')
        httpd.socket.close()

if __name__ == '__main__':
    main()
