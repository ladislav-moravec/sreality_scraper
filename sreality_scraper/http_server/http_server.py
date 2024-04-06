from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Definujeme data
data = [
    {"id": 2, "description": "Prodej bytu 4+1 99 m²", "price": "1 980 000 Kč",
     "images": ["https://sta-reality2.1gr.cz/sta/compile/thumbs/9/1/5/b9cc44adf6ae5495a1e8690408e3e.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/c/e/b/000b0f02d5d2fc214de38fe839725.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/0/a/a/0118ffdb12dc989d446821fa1ec23.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/6/3/d/0666f4654e1053041a17f67a9ad60.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/9/0/5/4aeb7ad9791dacd738a53713b01c8.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/c/b/6/4f5fe797906e2063df7c6610a0d09.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/b/6/2/9a3fa44551b0db45736c35862a013.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/c/9/c/2b0fe1db07e901e581fc122816724.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/6/1/9/7eb4efb3f70e16208a6b40b6cb056.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/6/f/1/6c68e3cddf77f7347a4757483f85d.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/3/a/0/d7de3edd7692ffbae1c9afbd6bed0.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/c/9/6/bde4c4133a2d4dc0a21c1fba6a8a4.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/f/c/d/47b56024f33369cd12abbe42624c0.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/b/e/8/da9373e54bddea4a0a8480a84af19.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/3/6/5/19c513633b44a4169ead522dee3eb.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/2/4/f/ec3a52d6b3dca55c35275b57f209e.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/e/f/f/999a843a71f1739a6a7e3f9065912.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/7/4/a/2726df6d86b8bd70be9efe4aa3084.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/b/c/2/56423b0b594c24bd069e8e7864ada.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/1/7/6/9cd2ed560c01885c85eb8ff5a9cd2.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/c/8/8/1077062d2efae3ca10aff6c07d874.jpg"]},
    {"id": 3, "description": "Prodej bytu 4+kk 88 m²", "price": "6 910 000 Kč",
     "images": ["https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e1?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e2?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e3?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e4?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e5?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e6?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e7?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e8?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66e9?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66ea?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66eb?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611c046c365b853df0c66ec?profile=front_detail_article_big"]},
    {"id": 4, "description": "Prodej bytu 2+1 14 545 m²", "price": "1 630 000 Kč",
     "images": ["https://sta-reality2.1gr.cz/sta/compile/thumbs/f/d/7/e566a184d3365927b332cdb1d9636.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/6/3/c/349b5d24b483f5efda4cb48966f5a.jpg",
                "https://reality.idnes.cz/file/thumbnail/6611b21785c073d4790e3d45?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611b21785c073d4790e3d46?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611b21785c073d4790e3d47?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611b21785c073d4790e3d48?profile=front_detail_article_big",
                "https://reality.idnes.cz/file/thumbnail/6611b21785c073d4790e3d49?profile=front_detail_article_big"]},
    {"id": 5, "description": "Prodej bytu 3+1 65 m²", "price": "5 280 000 Kč",
     "images": ["https://sta-reality2.1gr.cz/sta/compile/thumbs/f/5/c/e05fb26696f648ee698e94e4ce966.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/2/8/f/5394c68f7a304e10c206a24c1b06d.jpg",
                "https://sta-reality2.1gr.cz/sta/compile/thumbs/7/b/0/a1a339e6089d073812eb0494503c4.jpg"]}
]


# Třída obsluhující HTTP požadavky
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # Metoda pro zpracování GET požadavků
    def do_GET(self):
        # Nastavíme hlavičku odpovědi
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Pokud je požadavek na cestu '/', odešleme data
        if self.path == '/':
            self.wfile.write(json.dumps(data).encode())
        # Jinak odešleme 404 chybu
        else:
            self.send_error(404)


# Funkce pro spuštění HTTP serveru
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


# Spustíme HTTP server na portu 8000
run()