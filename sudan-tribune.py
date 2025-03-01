import cfscrape

scraper = cfscrape.create_scraper() 
print(scraper.get("https://sudantribune.com/").text)  
