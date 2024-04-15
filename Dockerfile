FROM python:3-alpine3.17
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD python ./sreality_scraper/postgresql/create_db.py
EXPOSE 8080
CMD python ./sreality_scraper/http_server/http_server_sreality.py
CMD python ./sreality_scraper/byty_sreality_api.py
EXPOSE 8081
CMD python ./sreality_scraper/http_server/http_server_idnes.py
CMD scrapy crawl idnes

