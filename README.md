## sreality_scraper .venv2
 
# run scrapers in spider florder to download data again
python -m scrapy crawl sreality
# or
python -m scrapy crawl idnes

# to see then start http server run 
python ./sreality_scraper/http_server/http_server_sreality.py @ port 8080
# or
python ./sreality_scraper/http_server/http_server_idnes.py # port 8081




# reqs
psycopg2