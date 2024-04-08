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
        cursor.execute("SELECT title, price, url_links FROM idnes_reality")
        rows = cursor.fetchall()

        # Format fetched data into HTML table rows and cells
        table_rows = ""
        for row in rows:
            table_rows += "<tr>"
            for idx, col in enumerate(row):
                if idx == len(row) - 1:  # Check if it's the last column
                    # Split the URLs and create <img> elements
                    image_urls = col.strip('{}').split(',')
                    images_html = ''.join([f'<img src="{url.strip()}">' for url in image_urls])
                    table_rows += f"<td>{images_html}</td>"
                else:
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
            <h1>Hello, World!</h1>
            <p>This is a simple HTTP server.</p>

            <h2>Sample Table</h2>
            <table border="1">
                <tr>
                    <th>Column 1</th>
                    <th>Column 2</th>
                    <th>Images</th>
                </tr>
                {table_rows}
            </table>

            <h2>Sample List</h2>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
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
