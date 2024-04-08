import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="master",
            user="postgres",
            password="asdf",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Execute query to fetch data from the database
        cursor.execute("SELECT * FROM idnes_reality")
        rows = cursor.fetchall()

        # Format fetched data into HTML table rows and cells
        table_rows = ""
        for row in rows:
            table_rows += "<tr>"
            for col in row:
                table_rows += f"<td>{col}</td>"
            table_rows += "</tr>"

        # Close database connection
        cursor.close()
        conn.close()

        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple HTTP Server</title>
        </head>
        <body>
            <h2>Idnes reality</h2>
            <table border="1">
                <tr>
                    <th>id</th>
                    <th>Titulek</th>
                    <th>Cena</th>
                    <th>Obrázky</th>
                    
                </tr>
                {table_rows}
            </table>

        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
