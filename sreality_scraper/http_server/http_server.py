import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/styles.css':  # Check if the requested path is for the CSS file
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('styles.css', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        page_number = int(query_components.get('page', ['1'])[0])
        rows_per_page = 10
        offset = (page_number - 1) * rows_per_page

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
        cursor.execute(f"SELECT * FROM idnes_reality LIMIT {rows_per_page} OFFSET {offset}")
        rows = cursor.fetchall()

        # Format fetched data into HTML table rows and cells
        table_rows = ""
        for row in rows:
            table_rows += "<tr>"
            table_rows += f"<td>{row[0]}</td>"  # id column
            table_rows += f"<td>{row[1]}</td>"  # Titulek column
            table_rows += f"<td>{row[2]}</td>"  # Cena column

            # Náhled column with only one picture and buttons for navigation
            image_urls = row[3][1:-1].split(",")  # Extract image URLs from string
            first_image_url = image_urls[0].strip()
            table_rows += f'<td><img id="image_{row[0]}" src="{first_image_url}">'
            table_rows += f'<br><button onclick="prevImage({row[0]}, {image_urls})">Previous</button>'
            table_rows += f'<button onclick="nextImage({row[0]}, {image_urls})">Next</button></td>'

            table_rows += "</tr>"

        # Count total number of rows in the database
        cursor.execute("SELECT COUNT(*) FROM idnes_reality")
        total_rows = cursor.fetchone()[0]

        # Calculate total number of pages
        total_pages = (total_rows + rows_per_page - 1) // rows_per_page

        # Close database connection
        cursor.close()
        conn.close()

        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple HTTP Server</title>
            <link rel="stylesheet" type="text/css" href="styles.css">
            <script>
                function prevImage(id, images) {{
                    var currentImage = document.getElementById('image_' + id);
                    var currentIndex = images.indexOf(currentImage.src);
                    if (currentIndex > 0) {{
                        currentImage.src = images[currentIndex - 1];
                    }}
                }}

                function nextImage(id, images) {{
                    var currentImage = document.getElementById('image_' + id);
                    var currentIndex = images.indexOf(currentImage.src);
                    if (currentIndex < images.length - 1) {{
                        currentImage.src = images[currentIndex + 1];
                    }}
                }}
            </script>
        </head>
        <body>
            <h1>Nabídky bytů v ČR</h1>

            <p>Jednoduchý náhled poskytl Ladislav Moravec</p>
            <table border="1">
                <tr>
                    <th>id</th>
                    <th>Titulek</th>
                    <th>Cena</th>
                    <th>Náhled</th>
                </tr>
                {table_rows}
            </table>

            <div>
                Page {page_number} of {total_pages}
                <br>
                {self.generate_pagination_links(page_number, total_pages)}
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def generate_pagination_links(self, current_page, total_pages):
        links = '<div class="pagination">'
        if current_page > 1:
            links += f'<a href="?page={current_page - 1}">Previous</a>'
        start_page = max(1, current_page - 5)  # Show 5 pages before the current page
        end_page = min(total_pages, start_page + 9)  # Show 10 pages in total
        for page_num in range(start_page, end_page + 1):
            if page_num == current_page:
                links += f'<span class="current">{page_num}</span>'
            else:
                links += f'<a href="?page={page_num}">{page_num}</a>'
        if current_page < total_pages:
            links += f'<a href="?page={current_page + 1}">Next</a>'
        links += '</div>'
        return links


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
